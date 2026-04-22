# kernel/coordinator/coordinator.py

import asyncio
from collections import deque

from kernel.task_manager.manager import TaskManager
from kernel.task_manager.models import TaskStatus
from kernel.context.context_builder import ContextBuilder

from kernel.execution.strategies.llm_executor import LLMExecutor
from kernel.execution.strategies.api_executor import APIExecutor

from kernel.core.logger import logger
from kernel.core.tracing import Trace
from kernel.core.config import Config
from kernel.core.limiter import ConcurrencyLimiter
from kernel.core.metrics import metrics


class KernelCoordinator:
    """
    KernelCoordinator — центральный оркестратор системы.

    Отвечает за:
    - жизненный цикл задачи
    - routing (через context)
    - retry
    - fallback
    - timeout
    - ограничение параллелизма
    - очередь задач
    - метрики и трассировку

    НЕ отвечает за:
    - выполнение (Executors)
    - построение контекста (ContextBuilder)
    - хранение задач (TaskManager)

    Это Control Plane системы.
    """

    def __init__(self):
        # =========================
        # Основные компоненты
        # =========================
        self.task_manager = TaskManager()
        self.context_builder = ContextBuilder()

        self.local_executor = LLMExecutor()
        self.api_executor = APIExecutor()

        # =========================
        # Ограничение параллелизма
        # =========================
        self.limiter = ConcurrencyLimiter()

        # =========================
        # Очередь задач (in-memory FIFO)
        # =========================
        self.queue = deque(maxlen=Config.MAX_QUEUE_SIZE)

        logger.info("[KERNEL INIT] KernelCoordinator initialized")

    # =========================
    # PUBLIC API
    # =========================
    async def handle_request(self, input_data: str):
        """
        Главная точка входа для API слоя

        :param input_data: входной текст
        :return: Task
        """

        # =========================
        # Валидация
        # =========================
        if len(input_data) > Config.MAX_INPUT_LENGTH:
            raise Exception("Input too large")

        # =========================
        # Создание задачи
        # =========================
        task = self.task_manager.create_task(input_data)

        # =========================
        # Трассировка
        # =========================
        trace = Trace(task.id)

        # =========================
        # Добавляем в очередь
        # =========================
        self.queue.append(task.id)

        # =========================
        # Ограничение параллелизма
        # =========================
        async with self.limiter:

            start_time = asyncio.get_event_loop().time()

            try:
                # =========================
                # Статус RUNNING
                # =========================
                self.task_manager.set_status(task.id, TaskStatus.RUNNING)

                # =========================
                # Строим context (routing внутри)
                # =========================
                context = self.context_builder.build(task)

                # =========================
                # Выполнение с retry + timeout
                # =========================
                result = await asyncio.wait_for(
                    self._execute_with_retry(context, task, trace),
                    timeout=Config.EXECUTION_TIMEOUT
                )

                # =========================
                # Успешное завершение
                # =========================
                self.task_manager.set_result(task.id, result)
                metrics.inc("completed")

            except asyncio.TimeoutError:
                # =========================
                # Timeout
                # =========================
                self.task_manager.set_status(task.id, TaskStatus.TIMEOUT)
                self.task_manager.set_error(task.id, "timeout")
                metrics.inc("timeout")

            except Exception as e:
                # =========================
                # Общая ошибка
                # =========================
                self.task_manager.set_error(task.id, str(e))
                metrics.inc("failed")

            finally:
                # =========================
                # Метрики времени
                # =========================
                duration = asyncio.get_event_loop().time() - start_time
                metrics.add_timing(duration)

        # =========================
        # Сохраняем trace
        # =========================
        task.context["trace"] = trace.to_dict()

        return task

    # =========================
    # INTERNAL LOGIC
    # =========================
    async def _execute_with_retry(self, context: dict, task, trace: Trace):
        """
        Выполнение задачи с retry и fallback

        :param context: execution context
        :param task: Task
        :param trace: Trace
        :return: результат выполнения
        """

        retries = 0

        while retries <= Config.MAX_RETRIES:
            try:
                # =========================
                # Выбор executor
                # =========================
                if context.get("execution_type") == "api":
                    executor = self.api_executor
                else:
                    executor = self.local_executor

                # =========================
                # Выполнение
                # =========================
                result = await executor.run(context)

                return result

            except Exception as e:
                retries += 1

                logger.warning(
                    f"[RETRY] task_id={task.id} attempt={retries} error={e}"
                )

                # =========================
                # Если превышен лимит retry
                # =========================
                if retries > Config.MAX_RETRIES:

                    # =========================
                    # Fallback → local executor
                    # =========================
                    if context.get("execution_type") == "api":
                        logger.warning(
                            f"[FALLBACK] task_id={task.id} switching to local"
                        )

                        try:
                            return await self.local_executor.run(context)
                        except Exception as fallback_error:
                            logger.exception(
                                f"[FALLBACK FAILED] task_id={task.id}"
                            )
                            raise fallback_error

                    # если уже local → пробрасываем ошибку
                    raise e

                # =========================
                # Статус RETRYING
                # =========================
                self.task_manager.set_status(task.id, TaskStatus.RETRYING)

                # =========================
                # Backoff (экспоненциальный)
                # =========================
                delay = Config.RETRY_BACKOFF ** retries
                await asyncio.sleep(delay)
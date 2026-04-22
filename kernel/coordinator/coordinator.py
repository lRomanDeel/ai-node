# kernel/coordinator/coordinator.py

from kernel.task_manager.manager import TaskManager
from kernel.task_manager.models import TaskStatus

from kernel.execution.strategies.llm_executor import LLMExecutor
from kernel.execution.strategies.api_executor import APIExecutor

from kernel.context.context_builder import ContextBuilder
from kernel.core.logger import logger
from kernel.core.tracing import Trace


class KernelCoordinator:
    """
    KernelCoordinator — центральный управляющий компонент системы.

    Отвечает за:
    - orchestration задач
    - управление жизненным циклом (FSM)
    - выбор execution пути (через context)
    - fallback стратегии

    НЕ отвечает за:
    - выполнение (делают executors)
    - выбор модели (делает ModelRouter)
    """

    def __init__(self):
        """
        Инициализация ядра
        """

        # =========================
        # Основные компоненты
        # =========================
        self.task_manager = TaskManager()
        self.context_builder = ContextBuilder()

        # =========================
        # Executors
        # =========================
        self.local_executor = LLMExecutor()
        self.api_executor = APIExecutor()

        logger.info("[KERNEL INIT] KernelCoordinator initialized")

    async def handle_request(self, input_data: str):
        """
        Основной pipeline выполнения задачи

        Pipeline:
        1. Create Task
        2. Build Context
        3. Route execution
        4. Execute (local / API)
        5. Fallback (если нужно)
        6. Save result
        7. Trace logging
        """

        logger.info(f"[REQUEST RECEIVED] input='{input_data}'")

        # =========================
        # 1. Создание задачи
        # =========================
        task = self.task_manager.create_task(input_data)

        # =========================
        # 2. Инициализация trace
        # =========================
        trace = Trace(task.id)

        try:
            # =========================
            # QUEUED
            # =========================
            span = trace.start_span("queue")
            self.task_manager.set_status(task.id, TaskStatus.QUEUED)
            span.finish()

            # =========================
            # RUNNING
            # =========================
            span = trace.start_span("run")
            self.task_manager.set_status(task.id, TaskStatus.RUNNING)
            span.finish()

            # =========================
            # CONTEXT BUILD
            # =========================
            span = trace.start_span("context_build")

            context = self.context_builder.build(task)

            span.set_metadata("model", context.get("model"))
            span.set_metadata("execution_type", context.get("execution_type"))

            span.finish()

            logger.info(
                f"[CONTEXT BUILT] task_id={task.id} "
                f"type={context.get('execution_type')} "
                f"model={context.get('model')}"
            )

            # =========================
            # EXECUTION
            # =========================
            span = trace.start_span("executor")

            result = None

            # --- PRIMARY EXECUTION ---
            if context.get("execution_type") == "api":
                try:
                    result = await self.api_executor.run(context)

                except Exception as e:
                    logger.warning(
                        f"[FALLBACK] API failed → switching to local. task_id={task.id}"
                    )

                    # fallback на локальную модель
                    result = await self.local_executor.run(context)

            else:
                result = await self.local_executor.run(context)

            span.finish()

            # =========================
            # RESULT
            # =========================
            span = trace.start_span("result")

            self.task_manager.set_result(task.id, result)

            span.finish()

        except Exception as e:
            # =========================
            # ERROR HANDLING
            # =========================
            logger.exception(f"[KERNEL ERROR] task_id={task.id}")

            error_span = trace.start_span("error")
            error_span.set_metadata("error", str(e))
            error_span.finish()

            self.task_manager.set_error(task.id, str(e))

        # =========================
        # TRACE LOGGING
        # =========================
        trace_data = trace.to_dict()

        logger.info(
            f"[TRACE] task_id={task.id} total={trace_data['total_duration']}s"
        )

        for span in trace_data["spans"]:
            logger.info(
                f"[SPAN] {span['name']} "
                f"duration={span['duration']}s "
                f"metadata={span['metadata']}"
            )

        # сохраняем trace
        task.context["trace"] = trace_data

        return task

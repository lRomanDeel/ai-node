# kernel/execution/strategies/llm_executor.py

from kernel.core.logger import logger


class LLMExecutor:
    """
    LLMExecutor — стратегия выполнения задач через LLM.

    Отвечает за:
    - вызов языковой модели
    - обработку входного контекста
    - возврат результата

    В текущей версии:
    - используется mock (заглушка)

    В будущем:
    - интеграция с Ollama (локальные модели)
    - интеграция с API (OpenAI, Claude и т.д.)
    - поддержка streaming
    """

    async def run(self, context: dict):
        """
        Основной метод выполнения задачи

        :param context: execution context (словарь с параметрами задачи)
        :return: результат выполнения (строка или структура)
        """

        # Извлекаем ключевые данные из контекста
        task_id = context.get("task_id")
        input_data = context.get("input")
        model = context.get("model")

        # Логируем старт выполнения
        logger.info(
            f"[EXECUTOR START] task_id={task_id} model={model}"
        )

        try:
            # =========================
            # MVP (заглушка выполнения)
            # =========================
            # Здесь пока просто имитируем работу LLM
            # Позже будет реальный вызов Ollama

            result = f"LLM processed: {input_data}"

            # =========================

            # Логируем успешное завершение
            logger.info(
                f"[EXECUTOR END] task_id={task_id}"
            )

            return result

        except Exception as e:
            # Логируем ошибку с трассировкой
            logger.exception(
                f"[EXECUTOR ERROR] task_id={task_id}"
            )

            # Пробрасываем ошибку выше (в Coordinator)
            raise e

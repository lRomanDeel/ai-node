# kernel/execution/strategies/llm_executor.py

import httpx
from kernel.core.logger import logger
from kernel.core.config import Config


class LLMExecutor:
    """
    LLMExecutor — выполнение задач через локальную модель (Ollama)

    Архитектурная роль:
    - выполнение "дешёвых" задач
    - fallback для API executor
    - основной исполнитель в оффлайн/low-cost режиме

    НЕ отвечает за:
    - routing (это делает ModelRouter)
    - retry (это делает Coordinator)
    - бизнес-логику

    Только выполнение.
    """

    def __init__(self):
        """
        Инициализация executor
        """

        # =========================
        # Ollama endpoint
        # =========================
        self.url = "http://127.0.0.1:11434/api/generate"

        # =========================
        # Таймаут (берём из config)
        # =========================
        self.timeout = Config.LOCAL_TIMEOUT

    async def run(self, context: dict):
        """
        Основной метод выполнения задачи

        :param context: execution context
        :return: результат выполнения (строка)
        """

        # =========================
        # Извлекаем данные из контекста
        # =========================
        task_id = context.get("task_id")
        input_data = context.get("input")
        model = context.get("model")

        logger.info(
            f"[LOCAL EXECUTOR START] task_id={task_id} model={model}"
        )

        try:
            # =========================
            # Формируем payload для Ollama
            # =========================
            payload = {
                "model": model,
                "prompt": input_data,
                "stream": False  # MVP — без streaming
            }

            # =========================
            # HTTP запрос к Ollama
            # =========================
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    self.url,
                    json=payload
                )

            # =========================
            # Проверка ответа
            # =========================
            if response.status_code != 200:
                raise Exception(
                    f"Ollama error: {response.text}"
                )

            data = response.json()

            # =========================
            # Извлекаем результат
            # =========================
            result = data.get("response")

            if not result:
                raise Exception("Empty response from Ollama")

            logger.info(
                f"[LOCAL EXECUTOR END] task_id={task_id}"
            )

            return result

        except Exception as e:
            # =========================
            # Логируем ошибку
            # =========================
            logger.exception(
                f"[LOCAL EXECUTOR ERROR] task_id={task_id}"
            )

            # пробрасываем выше (Coordinator решает retry/fallback)
            raise e
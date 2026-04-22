# kernel/execution/strategies/api_executor.py

import os
import httpx

from dotenv import load_dotenv
from kernel.core.logger import logger


# =========================
# Загружаем переменные окружения из .env
# =========================
load_dotenv()


class APIExecutor:
    """
    APIExecutor — выполнение задач через внешние LLM API.

    Архитектурная роль:
    - выполнение сложных задач
    - получение более качественных ответов
    - fallback для локальных моделей (в будущем)

    Поддержка:
    - OpenAI API (текущая реализация)
    - легко расширяется (Claude, Gemini и т.д.)
    """

    def __init__(self):
        """
        Инициализация API executor
        """

        # =========================
        # Получение API ключа
        # =========================
        self.api_key = os.getenv("OPENAI_API_KEY")

        if not self.api_key:
            logger.warning("[API EXECUTOR] OPENAI_API_KEY not found")

        # =========================
        # Endpoint OpenAI
        # =========================
        self.url = "https://api.openai.com/v1/chat/completions"

        # =========================
        # Таймаут (сек)
        # =========================
        self.timeout = 60.0

    async def run(self, context: dict):
        """
        Выполнение задачи через API

        :param context: execution context
        :return: результат выполнения (строка)
        """

        task_id = context.get("task_id")
        input_data = context.get("input")

        logger.info(f"[API EXECUTOR START] task_id={task_id}")

        try:
            # =========================
            # Проверка ключа
            # =========================
            if not self.api_key:
                raise Exception("OPENAI_API_KEY is not set")

            # =========================
            # Заголовки запроса
            # =========================
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }

            # =========================
            # Тело запроса
            # =========================
            payload = {
                "model": "gpt-4o-mini",  # быстрый и дешевый вариант
                "messages": [
                    {
                        "role": "user",
                        "content": input_data
                    }
                ],
                "temperature": 0.7
            }

            # =========================
            # Выполнение HTTP запроса
            # =========================
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    self.url,
                    headers=headers,
                    json=payload
                )

            # =========================
            # Проверка ответа
            # =========================
            if response.status_code != 200:
                raise Exception(f"API error: {response.text}")

            data = response.json()

            # =========================
            # Извлечение результата
            # =========================
            result = data["choices"][0]["message"]["content"]

            logger.info(f"[API EXECUTOR END] task_id={task_id}")

            return result

        except Exception as e:
            # =========================
            # Логирование ошибки
            # =========================
            logger.exception(f"[API EXECUTOR ERROR] task_id={task_id}")

            # пробрасываем ошибку выше (Coordinator решает fallback)
            raise e
# kernel/execution/strategies/api_executor.py

import os
import httpx

from dotenv import load_dotenv
from kernel.core.logger import logger
from kernel.core.config import Config

# =========================
# Загружаем переменные окружения (.env)
# =========================
load_dotenv()


class APIExecutor:
    """
    APIExecutor — выполнение задач через внешние LLM API (OpenAI)

    Архитектурная роль:
    - выполнение сложных задач
    - high-quality ответы
    - fallback target для routing (если выбран API)

    НЕ отвечает за:
    - retry (Coordinator)
    - fallback (Coordinator)
    - routing (ModelRouter)
    - бизнес-логику

    Только выполнение запроса к API.
    """

    def __init__(self):
        """
        Инициализация executor
        """

        # =========================
        # API ключ (из .env)
        # =========================
        self.api_key = os.getenv("OPENAI_API_KEY")

        if not self.api_key:
            logger.warning("[API EXECUTOR] OPENAI_API_KEY not found")

        # =========================
        # Endpoint OpenAI
        # =========================
        self.url = "https://api.openai.com/v1/chat/completions"

        # =========================
        # Таймаут из config
        # =========================
        self.timeout = Config.API_TIMEOUT

    async def run(self, context: dict):
        """
        Основной метод выполнения задачи через API

        :param context: execution context
        :return: результат выполнения (строка)
        """

        # =========================
        # Извлекаем данные из context
        # =========================
        task_id = context.get("task_id")
        input_data = context.get("input")
        model = context.get("model", "gpt-4o-mini")

        logger.info(
            f"[API EXECUTOR START] task_id={task_id} model={model}"
        )

        try:
            # =========================
            # Проверка API ключа
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
            # Формируем payload
            # =========================
            payload = {
                "model": model,
                "messages": [
                    {
                        "role": "user",
                        "content": input_data
                    }
                ],
                "temperature": 0.7
            }

            # =========================
            # HTTP запрос
            # =========================
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    self.url,
                    headers=headers,
                    json=payload
                )

            # =========================
            # Проверка ответа API
            # =========================
            if response.status_code != 200:
                raise Exception(
                    f"API error: {response.status_code} {response.text}"
                )

            data = response.json()

            # =========================
            # Извлекаем результат
            # =========================
            try:
                result = data["choices"][0]["message"]["content"]
            except Exception:
                raise Exception(f"Invalid API response format: {data}")

            if not result:
                raise Exception("Empty response from API")

            logger.info(
                f"[API EXECUTOR END] task_id={task_id}"
            )

            return result

        except Exception as e:
            # =========================
            # Логируем ошибку
            # =========================
            logger.exception(
                f"[API EXECUTOR ERROR] task_id={task_id}"
            )

            # ВАЖНО:
            # не обрабатываем здесь → Coordinator решает retry/fallback
            raise e
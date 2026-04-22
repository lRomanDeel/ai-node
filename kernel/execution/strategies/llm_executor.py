# kernel/execution/strategies/llm_executor.py

import httpx
from kernel.core.logger import logger


class LLMExecutor:
    """
    LLMExecutor — стратегия выполнения задач через локальную LLM (Ollama)

    Отвечает за:
    - отправку prompt в Ollama
    - получение ответа модели
    - обработку ошибок

    Архитектурно:
    - это одна из стратегий Execution Layer
    - в будущем можно добавить:
        - AgentExecutor
        - WorkflowExecutor (LangGraph)
        - ToolExecutor
    """

    def __init__(self):
        """
        Инициализация executor'а
        """
        # Endpoint Ollama API
        self.ollama_url = "http://localhost:11434/api/generate"

        # Таймаут на генерацию (важно для CPU)
        self.timeout = 300.0  # секунд

    async def run(self, context: dict):
        """
        Основной метод выполнения задачи

        :param context: execution context (данные задачи)
        :return: результат генерации модели
        """

        # =========================
        # Извлекаем данные из контекста
        # =========================
        task_id = context.get("task_id")
        input_data = context.get("input")
        model = context.get("model", "llama3:8b")

        logger.info(f"[EXECUTOR START] task_id={task_id} model={model}")

        try:
            # =========================
            # Формируем запрос к Ollama
            # =========================
            payload = {
                "model": model,
                "prompt": input_data,
                "stream": False  # пока без стриминга
            }

            # =========================
            # Асинхронный HTTP запрос
            # =========================
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(self.ollama_url, json=payload)

            # =========================
            # Проверка ответа
            # =========================
            if response.status_code != 200:
                raise Exception(f"Ollama error: {response.text}")

            data = response.json()

            # Ollama возвращает результат в поле "response"
            result = data.get("response", "")

            # =========================
            # Лог успешного выполнения
            # =========================
            logger.info(f"[EXECUTOR END] task_id={task_id}")

            return result

        except httpx.RequestError as e:
            # Ошибка сети / соединения
            logger.exception(f"[EXECUTOR NETWORK ERROR] task_id={task_id}")
            raise Exception("Failed to connect to Ollama") from e

        except Exception as e:
            # Общая ошибка выполнения
            logger.exception(f"[EXECUTOR ERROR] task_id={task_id}")
            raise e

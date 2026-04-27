"""
Execution Layer (MVP → upgraded with streaming)

Назначение:
- принять execution context
- сформировать prompt
- вызвать модель (Ollama)
- вернуть ответ

ВАЖНО:
- добавлен streaming (чтобы не было таймаутов)
- сохранена архитектура
- без усложнений (MVP+)

Этап: 5 (Context & Knowledge Layer)
"""

import requests
import json


class Executor:
    def __init__(self):
        """
        Инициализация executor
        """
        self.ollama_url = "http://localhost:11434/api/generate"

    # --------------------------------------------------
    # MAIN ENTRY POINT
    # --------------------------------------------------
    def execute(self, context: dict) -> str:
        """
        Выполнение задачи

        :param context: execution context
        :return: текст ответа модели
        """

        prompt = self._build_prompt(context)
        model = context["model"]

        print(f"🧠 Using model: {model}")
        print("🤖 GENERATING RESPONSE...")

        try:
            return self._call_ollama_stream(model, prompt)

        except Exception as e:
            return f"❌ Execution failed: {str(e)}"

    # --------------------------------------------------
    # PROMPT BUILDER
    # --------------------------------------------------
    def _build_prompt(self, context: dict) -> str:
        """
        Формирует prompt

        Упрощён специально:
        - меньше токенов
        - быстрее генерация
        """

        input_text = context["input"]
        rag_context = context.get("rag_context", "")

        # если есть RAG → используем
        if rag_context:
            return f"""
Context:
{rag_context}

Question:
{input_text}

Answer briefly:
""".strip()

        # если нет RAG
        return f"""
Question:
{input_text}

Answer briefly:
""".strip()

    # --------------------------------------------------
    # OLLAMA STREAMING CALL (КЛЮЧЕВОЕ ИЗМЕНЕНИЕ)
    # --------------------------------------------------
    def _call_ollama_stream(self, model: str, prompt: str) -> str:
        """
        Streaming вызов Ollama

        Почему это важно:
        - НЕ ждём весь ответ
        - получаем токены сразу
        - избегаем timeout
        """

        response = requests.post(
            self.ollama_url,
            json={
                "model": model,
                "prompt": prompt,
                "stream": True,  # 🔥 ВАЖНО
                "options": {
                    "num_predict": 120,  # ограничение длины
                    "temperature": 0.3
                }
            },
            stream=True  # 🔥 ВАЖНО
        )

        if response.status_code != 200:
            raise Exception(response.text)

        full_response = ""

        print("\n💬 Streaming response:\n")

        # читаем поток
        for line in response.iter_lines():

            if not line:
                continue

            try:
                data = json.loads(line.decode("utf-8"))

                token = data.get("response", "")

                # выводим сразу (живой ответ)
                print(token, end="", flush=True)

                full_response += token

            except Exception:
                # иногда приходят служебные куски → игнор
                pass

        print("\n")

        return full_response.strip()
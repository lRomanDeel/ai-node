# kernel/execution/model_router.py

from kernel.core.logger import logger


class ModelRouter:
    """
    ModelRouter — слой принятия решения (Decision Layer).

    Отвечает за:
    - выбор типа выполнения задачи (local / api)
    - выбор модели
    - баланс между скоростью, стоимостью и качеством

    Архитектурная роль:
    - отделяет бизнес-логику выбора модели от execution
    - позволяет гибко масштабировать систему

    В будущем сюда добавится:
    - intent classification (ML)
    - user tier (free / paid)
    - rate limiting
    - fallback стратегии
    """

    def route(self, context: dict) -> dict:
        """
        Определяет, как выполнять задачу

        :param context: execution context
        :return: dict:
        {
            "type": "local" | "api",
            "model": str
        }
        """

        task_type = context.get("task_type", "simple")
        input_text = context.get("input", "")

        # =========================
        # 1. Базовая логика routing
        # =========================

        if task_type == "simple":
            route = {
                "type": "local",
                "model": "phi3:latest"
            }

        elif task_type == "normal":
            route = {
                "type": "local",
                "model": "llama3:8b"
            }

        elif task_type == "complex":
            route = {
                "type": "api",
                "model": "gpt-4o-mini"
            }

        else:
            # fallback безопасный вариант
            route = {
                "type": "local",
                "model": "phi3:latest"
            }

        # =========================
        # 2. Дополнительные эвристики
        # =========================
        # Пример: если текст очень длинный → лучше API

        if len(input_text) > 1000:
            route = {
                "type": "api",
                "model": "gpt-4o-mini"
            }

        # =========================
        # 3. Логирование решения
        # =========================

        logger.info(
            f"[MODEL ROUTER] task_type={task_type} "
            f"input_len={len(input_text)} "
            f"→ type={route['type']} model={route['model']}"
        )

        return route

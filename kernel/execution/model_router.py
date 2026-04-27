# kernel/execution/model_router.py

from kernel.core.logger import logger


class ModelRouter:
    """
    ModelRouter — слой принятия решения (Decision Layer)

    Отвечает за:
    - выбор типа выполнения (local / api)
    - выбор модели

    ВАЖНО:
    На CPU используем лёгкие модели (phi3),
    иначе система становится непригодной по скорости.
    """

    def route(self, context: dict) -> dict:
        """
        Определяет стратегию выполнения задачи
        """

        task_type = context.get("task_type", "simple")
        input_text = context.get("input", "")

        # =========================
        # 1. Базовая логика routing
        # =========================

        # 🔥 ВСЕ local задачи → лёгкая модель
        if task_type == "simple":
            route = {
                "type": "local",
                "model": "phi3:latest"
            }

        elif task_type == "normal":
            route = {
                "type": "local",
                "model": "tinyllama"  # 🔥 было llama3:8b → заменили
            }

        elif task_type == "complex":
            route = {
                "type": "api",
                "model": "gpt-4o-mini"
            }

        else:
            route = {
                "type": "local",
                "model": "phi3:latest"
            }

        # =========================
        # 2. Дополнительные эвристики
        # =========================

        # 🔥 длинный текст → API
        if len(input_text) > 1000:
            route = {
                "type": "api",
                "model": "gpt-4o-mini"
            }

        # =========================
        # 3. Логирование
        # =========================

        logger.info(
            f"[MODEL ROUTER] task_type={task_type} "
            f"input_len={len(input_text)} "
            f"→ type={route['type']} model={route['model']}"
        )

        return route
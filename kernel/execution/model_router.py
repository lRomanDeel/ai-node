"""
Model Router (Deterministic)

Назначение:
- выбрать модель по конфигурации

Архитектурная роль:
- НЕ содержит эвристик
- НЕ принимает "умных" решений
- просто читает MODEL_REGISTRY

Это делает систему:
✔ предсказуемой
✔ контролируемой
✔ production-ready
"""

from kernel.config.model_registry import MODEL_REGISTRY
from kernel.core.logger import logger


class ModelRouter:
    def route(self, context: dict) -> dict:
        """
        Возвращает модель для выполнения задачи

        :param context: execution context
        :return: dict:
        {
            "type": "local" | "api",
            "model": str
        }
        """

        task_type = context.get("task_type", "simple")

        # =========================
        # ЖЁСТКОЕ СООТВЕТСТВИЕ
        # =========================
        route = MODEL_REGISTRY.get(task_type)

        # fallback (на всякий случай)
        if not route:
            route = MODEL_REGISTRY["simple"]

        # логирование (очень важно для отладки)
        logger.info(
            f"[MODEL ROUTER] task_type={task_type} "
            f"→ type={route['type']} model={route['model']}"
        )

        return route
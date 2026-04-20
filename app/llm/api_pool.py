class ApiPool:
    def __init__(self, config):
        self.config = config

    async def generate(self, model_name: str, prompt: str) -> str:
        # Заглушка для API моделей
        return f"[API:{model_name}] {prompt[:80]}"

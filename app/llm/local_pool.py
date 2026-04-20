class LocalPool:
    def __init__(self, config):
        self.config = config

    async def generate(self, model_name: str, prompt: str) -> str:
        # Заглушка для локальных моделей
        return f"[LOCAL:{model_name}] {prompt[:80]}"

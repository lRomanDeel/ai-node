import yaml
from app.llm.local_pool import LocalPool
from app.llm.api_pool import ApiPool


class LLMRouter:
    def __init__(self, config_path="app/config/models.yaml"):
        with open(config_path, "r") as f:
            self.config = yaml.safe_load(f)

        self.local_pool = LocalPool(self.config)
        self.api_pool = ApiPool(self.config)

    async def generate(self, role: str, prompt: str) -> str:
        mode = self.config["mode"][role]

        if mode == "local":
            model_name = self.config["local_models"][role]
            return await self.local_pool.generate(model_name, prompt)

        if mode == "api":
            model_name = self.config["api_models"][role]
            return await self.api_pool.generate(model_name, prompt)

        raise ValueError(f"Unknown mode: {mode}")

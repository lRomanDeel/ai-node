class BaseLLM:
    async def generate(self, prompt: str, role: str) -> str:
        raise NotImplementedError

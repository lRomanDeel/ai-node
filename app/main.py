import asyncio
from app.llm.router import LLMRouter


async def test():
    router = LLMRouter()

    result_editor = await router.generate(
        role="editor",
        prompt="This is a test article about AI automation."
    )

    result_analyzer = await router.generate(
        role="analyzer",
        prompt="Analyze this text."
    )

    print(result_editor)
    print(result_analyzer)


asyncio.run(test())

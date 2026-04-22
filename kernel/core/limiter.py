# kernel/core/limiter.py

import asyncio
from kernel.core.config import Config


class ConcurrencyLimiter:
    """
    Ограничивает количество одновременных задач
    """
    def __init__(self):
        self._sem = asyncio.Semaphore(Config.MAX_CONCURRENT_TASKS)

    async def __aenter__(self):
        await self._sem.acquire()

    async def __aexit__(self, exc_type, exc, tb):
        self._sem.release()

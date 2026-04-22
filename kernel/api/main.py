# kernel/api/main.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from kernel.coordinator.coordinator import KernelCoordinator
from kernel.core.logger import logger
from kernel.core.metrics import metrics


# =========================
# Инициализация FastAPI
# =========================
app = FastAPI(
    title="AI Kernel API",
    description="Core orchestration layer for AI system",
    version="1.0.0"
)

# =========================
# Инициализация ядра
# =========================
coordinator = KernelCoordinator()


# =========================
# Request модель
# =========================
class TaskRequest(BaseModel):
    """
    Входная модель запроса

    input — текст задачи
    """
    input: str


# =========================
# Response модель (опционально)
# =========================
class TaskResponse(BaseModel):
    id: str
    input_data: str
    status: str
    result: str | None = None
    error: str | None = None
    context: dict


# =========================
# ROOT endpoint
# =========================
@app.get("/")
async def root():
    """
    Базовая проверка, что API работает
    """
    return {"status": "kernel is running"}


# =========================
# HEALTH endpoint
# =========================
@app.get("/health")
async def health():
    """
    Health-check + метрики

    Используется для:
    - мониторинга
    - проверки состояния системы
    """

    return {
        "status": "ok",
        "metrics": metrics.snapshot()
    }


# =========================
# MAIN endpoint
# =========================
@app.post("/task", response_model=TaskResponse)
async def create_task(request: TaskRequest):
    """
    Основной endpoint системы

    Поток:
    API → Coordinator → Kernel → Executors → Result

    :param request: TaskRequest
    :return: TaskResponse
    """

    try:
        logger.info(f"[API REQUEST] input={request.input[:50]}")

        # =========================
        # Передаём задачу в ядро
        # =========================
        task = await coordinator.handle_request(request.input)

        # =========================
        # Формируем ответ
        # =========================
        return TaskResponse(
            id=task.id,
            input_data=task.input_data,
            status=task.status,
            result=task.result,
            error=task.error,
            context=task.context
        )

    except Exception as e:
        logger.exception("[API ERROR]")

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
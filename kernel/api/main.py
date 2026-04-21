# kernel/api/main.py

# kernel/api/main.py

from fastapi import FastAPI
from pydantic import BaseModel

from kernel.coordinator.coordinator import KernelCoordinator


# Инициализация приложения
app = FastAPI()

# Инициализация ядра
kernel = KernelCoordinator()


class TaskRequest(BaseModel):
    """
    Модель входящего запроса
    """
    input: str


@app.get("/")
async def root():
    """
    Проверка работоспособности API
    """
    return {"status": "kernel is running"}


@app.post("/task")
async def create_task(req: TaskRequest):
    """
    Создание и выполнение задачи
    """
    return await kernel.handle_request(req.input)

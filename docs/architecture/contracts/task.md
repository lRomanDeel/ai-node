# Task Contract

Task — базовая единица выполнения в системе AI Content Engine.

Любое действие в системе начинается с создания Task.
Ни один агент не вызывается напрямую — только через Task.

---

# 1. Назначение

Task описывает:

- Что нужно сделать
- В каком проекте
- Каким workflow
- С какими входными данными
- В каком состоянии находится выполнение

Task является единственной точкой входа в Kernel.

---

# 2. Структура Task

## Обязательные поля

- id: UUID
- project_id: string
- workflow_id: string
- intent: string
- input_payload: JSON
- priority: integer
- status: enum
- created_at: timestamp
- updated_at: timestamp

---

## Дополнительные поля

- parent_task_id: UUID (для вложенных задач)
- retry_count: integer
- max_retries: integer
- requires_approval: boolean
- budget_snapshot: JSON
- policy_snapshot: JSON
- version: string

---

# 3. Статусы Task

Task может находиться в одном из состояний:

- CREATED
- QUEUED
- RUNNING
- WAITING_APPROVAL
- COMPLETED
- FAILED
- CANCELLED

Статус изменяется только через Kernel.

---

# 4. Принципы работы

1. Task неизменяем по intent.
2. Workflow не может менять intent.
3. Агент не может менять статус Task напрямую.
4. Kernel управляет жизненным циклом Task.
5. Каждое изменение статуса логируется.
6. Каждое выполнение версии workflow фиксируется.

---

# 5. Жизненный цикл Task

1. Создание Task
2. Проверка Project и Budget
3. Присвоение Workflow
4. Выполнение шагов
5. (Опционально) Human approval
6. Завершение или ошибка
7. Логирование и архивирование

---

# 6. Связь с другими слоями

Task взаимодействует с:

- Kernel (управление)
- Context Layer (формирование контекста)
- Workflow Layer (порядок выполнения)
- Agents Layer (исполнение)
- Observability Layer (логирование)
- Human Layer (approval)
- Versioning Layer (фиксация версии выполнения)

---

# 7. Архитектурные гарантии

- Task — атомарная единица работы.
- Каждый Task привязан к конкретному проекту.
- Task не может существовать вне Project.
- Все действия воспроизводимы по логам.

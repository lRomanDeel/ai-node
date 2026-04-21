# Task Lifecycle

## Flow

1. CREATED — задача создана
2. QUEUED — добавлена в очередь
3. RUNNING — выполняется
4. WAITING — ожидает внешнего действия
5. COMPLETED / FAILED — завершение

---

## Diagram
CREATED
↓
QUEUED
↓
RUNNING
↓
WAITING → RUNNING
↓
COMPLETED / FAILED


---

## Notes

WAITING используется для:
- tool execution
- human input
- external API

---

## Guarantees

- задача не может перескочить состояния
- все переходы валидируются FSM

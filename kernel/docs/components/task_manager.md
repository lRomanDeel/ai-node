# Task Manager

## Role

Управляет жизненным циклом задач.

---

## Responsibilities

- хранение задач
- управление статусами
- контроль переходов состояний (FSM)

---

## State Machine

CREATED → QUEUED → RUNNING → WAITING → COMPLETED / FAILED

---

## Guarantees

- все задачи проходят через Task Manager
- все переходы валидируются
- невозможны некорректные состояния

---

## Storage (v1)

- In-memory dictionary

---

## Future

- PostgreSQL persistence
- task history
- retries
- priorities


# Kernel Coordinator

## Role

Центральная точка входа в ядро.

---

## Responsibilities

- принимает запросы
- создаёт задачи
- формирует execution context
- передаёт задачу в Task Manager

---

## Not Responsible For

- выполнение задач
- хранение состояния
- бизнес-логика агентов

---

## Flow

1. Получить input
2. Создать Task
3. Передать в Task Manager
4. Инициировать выполнение

---

## Future Responsibilities

- routing задач
- выбор executor
- multi-agent orchestration

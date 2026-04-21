# Kernel Architecture Overview

## Purpose

Kernel — orchestration engine системы AI Node.

---

## High-Level Architecture
User / API
↓
Kernel Coordinator
↓
Task Manager (FSM)
↓
Execution Layer
↓
Agents / LLM / Tools / RAG


---

## Core Responsibilities

- управление задачами
- контроль выполнения
- маршрутизация (в будущем)
- подготовка execution context

---

## Key Design Decisions

### 1. State Machine First
Все задачи управляются через FSM.

### 2. Async Execution
Все операции ядра асинхронны.

### 3. Execution Abstraction
Ядро не зависит от:
- моделей
- агентов
- инструментов

---

## Future Extensions

- LangGraph integration
- Multi-agent routing
- Distributed execution
- Queue system (Redis)

---

## Constraints (v1)

- In-memory storage
- Single node execution
- No task prioritization


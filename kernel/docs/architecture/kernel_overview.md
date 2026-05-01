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

---

# Stage 5 — Context & Knowledge Layer (COMPLETED ✅)

## 📌 Overview

Реализован полный RAG pipeline:

Task → Context → Knowledge → Prompt → Execution → Response

---

## 🧩 Components

### Retriever
- Использует SentenceTransformers (all-MiniLM-L6-v2)
- Интеграция с Qdrant (vector search)
- Новый API: query_points

---

### KnowledgeBuilder
- Преобразует raw retrieval → structured knowledge
- Фильтрация по score (MVP threshold ~0.1)
- Формат:

```json
{
  "documents": [
    {"text": "...", "score": 0.16}
  ],
  "metadata": {
    "source": "qdrant",
    "count": 1
  }
}

    ContextBuilder
Собирает execution context
Интегрирует:
input
knowledge
routing (model selection)

    PromptBuilder
Формирует строго контролируемый prompt
Поддерживает RAG-only режим
Запрещает использование внешних знаний

    Executor
Выполняет генерацию
Реализует HARD GUARDRAIL

if not documents:
    return "I don't know based on the provided context."

🛡 Guardrails
    Реализована защита от hallucination:
        если knowledge пустой → модель НЕ вызывается
        deterministic fallback

🧪 Tests
    TEST 1 (RAG)
        документы извлекаются
        используются в prompt
        модель отвечает по контексту
    TEST 2 (No Context)
        knowledge = empty
        ответ:
        "I don't know based on the provided context."

📊 Result
    Retrieval: ✔
    Knowledge processing: ✔
    Context system: ✔
    Prompt control: ✔
    Execution safety: ✔

🚀 Status

Stage 5: COMPLETED ✔


➡ Next Stage
    Stage 6 — Intelligence Layer:
        multi-model routing
        roles (editor / researcher)
        agents & strategies


---

# 💡 ПОЧЕМУ ИМЕННО ТАК

Ты не создаёшь 100 файлов, а:

```text
держишь архитектуру в одном месте → kernel_overview.md
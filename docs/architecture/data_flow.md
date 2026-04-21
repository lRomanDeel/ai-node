# AI Content Engine — Data Flow

## 1. Общая схема

User / System Trigger
        ↓
Project
        ↓
Kernel
        ↓
Workflow
        ↓
Context Builder
        ↓
Agent
        ↓
LLM Router
        ↓
Model (Local / API)
        ↓
Result
        ↓
Human Layer
        ↓
Persistence + Observability


---

# 3. Контракты между слоями

## Task Contract

Любой процесс начинается с Task.

Task содержит:

- id
- project_id
- workflow_id
- intent
- input_payload
- priority
- status
- created_at

Task — единственная точка входа в систему.

---

## Context Contract

Перед каждым вызовом агента формируется Context:

- project_static_context
- dynamic_memory
- relevant_embeddings
- policy_constraints
- budget_state

Context не хранится в агенте.
Он создаётся каждый раз заново.

---

## AgentResult Contract

Каждый агент возвращает структурированный результат:

- agent_name
- raw_output
- structured_output
- tokens_used
- cost_estimate
- execution_time
- version

Kernel обрабатывает только AgentResult.

---

# 4. Обратные потоки (Feedback Flow)

После выполнения шага:

- результат сохраняется
- memory обновляется
- бюджет обновляется
- observability логируется

Если включён Human Layer:

- создаётся approval task
- возможен override
- изменения записываются в versioning

---

# 5. Архитектурные принципы

1. Ни один агент не вызывается напрямую.
2. Контекст формируется перед каждым вызовом.
3. Kernel — единственная точка координации.
4. Каждый шаг логируется.
5. Каждый вызов LLM фиксируется.
6. Каждое изменение версионируется.
7. Любое расширение сопровождается документацией.

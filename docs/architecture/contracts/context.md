# Context Contract

Context — структурированный пакет данных,
который формируется перед каждым вызовом агента.

Context не хранится внутри агента.
Он создаётся Context Layer на основе Project + Task.

---

# 1. Назначение

Context обеспечивает:

- Актуальность информации
- Контроль размера input
- Изоляцию проектов
- Предотвращение context drift

---

# 2. Структура Context

## Основные блоки

- project_static_context: JSON
- dynamic_memory: JSON
- semantic_memory: JSON
- policy_constraints: JSON
- budget_state: JSON
- execution_metadata: JSON

---

## project_static_context

Содержит:

- tone_of_voice
- target_audience
- strategic_goals
- content_rules
- forbidden_topics

---

## dynamic_memory

Содержит:

- последние N действий
- последние публикации
- активные гипотезы
- текущие KPI

---

## semantic_memory

Vector-based retrieval:

- релевантные прошлые посты
- стилистические примеры
- обучающие фрагменты

Ограничение по размеру — обязательное.

---

## policy_constraints

- max_tokens
- temperature_limit
- cost_limit
- approval_required

---

## budget_state

- budget_remaining
- cost_per_step
- monthly_limit
- warning_flags

---

## execution_metadata

- task_id
- workflow_id
- agent_version
- timestamp

---

# 3. Принципы

1. Context формируется заново перед каждым вызовом.
2. Размер Context ограничивается.
3. Context не мутируется агентом.
4. Context не хранится как глобальное состояние.
5. Контекст зависит от Project scope.

---

# 4. Архитектурные гарантии

- Context изолирован по проектам.
- Context не может утечь в другой проект.
- Context не хранится в памяти агента.

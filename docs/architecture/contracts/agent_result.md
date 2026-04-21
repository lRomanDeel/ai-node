# AgentResult Contract

AgentResult — структурированный результат выполнения агента.

Kernel принимает только AgentResult.
Никакой сырой текст не передаётся напрямую между слоями.

---

# 1. Назначение

AgentResult обеспечивает:

- Стандартизацию результата
- Логирование
- Учёт токенов
- Учёт стоимости
- Версионирование выполнения

---

# 2. Структура AgentResult

## Основные поля

- agent_name: string
- task_id: UUID
- raw_output: string
- structured_output: JSON
- tokens_input: integer
- tokens_output: integer
- total_tokens: integer
- cost_estimate: float
- execution_time_ms: integer
- model_used: string
- agent_version: string
- timestamp: timestamp

---

# 3. structured_output

Агент обязан возвращать:

- cleaned_text
- metadata
- confidence_score
- warnings

Формат structured_output зависит от типа агента,
но структура должна быть валидируемой.

---

# 4. Принципы

1. Agent не меняет Task напрямую.
2. Agent не сохраняет результат в базу напрямую.
3. Agent возвращает только AgentResult.
4. Kernel решает, что делать с результатом.

---

# 5. Связь с другими слоями

AgentResult передаётся в:

- Kernel (обработка)
- Observability (логирование)
- Versioning (фиксация версии)
- Context Layer (обновление памяти)
- Human Layer (если требуется approval)

---

# 6. Архитектурные гарантии

- Каждый вызов агента фиксируется.
- Стоимость и токены логируются.
- Версия агента сохраняется.
- Результат воспроизводим.

# Execution Layer

## Role

Абстракция выполнения задач.

---

## Purpose

Изолировать ядро от:
- LLM
- агентов
- workflow движков

---

## Types of Executors

- LLM Executor
- Agent Executor
- Workflow Executor (LangGraph)

---

## Design Principle

Strategy Pattern

---

## Context Input
{
"task_id": "...",
"input": "...",
"model": "...",
"tools": [],
"memory_refs": []
}


---

## Future

- dynamic executor selection
- tool calling
- chain execution

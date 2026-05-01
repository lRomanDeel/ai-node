# AI Media System — Documentation

## Version
v0.4 — Kernel MVP+ (Stage 4 completed)

## Overview
Система представляет собой AI orchestration platform:
- Kernel (control plane)
- Execution layer (LLM)
- Knowledge layer (RAG — upcoming)

---

## Architecture

- [Layers](architecture/layers.md)
- [Data Flow](architecture/data_flow.md)

---

## Kernel

- [Overview](../kernel/docs/architecture/kernel_overview.md)
- [Components](../kernel/docs/components/)
- [Flows](../kernel/docs/flows/)

---

## Contracts

- [Task](architecture/contracts/task.md)
- [Context](architecture/contracts/context.md)
- [Agent Result](architecture/contracts/agent_result.md)

---

## Current Status

Stage 4 completed:
- Kernel orchestration
- Hybrid execution
- Retry / fallback / timeout
- Observability

---

## Next Stage

Stage 5:
Knowledge Layer (RAG)






## Internal Modules Documentation

- Kernel:
  - ../kernel/docs/README.md




AI Media System — Documentation
Version

v0.5 — Agents Pipeline (in progress)

🧠 Overview

AI Media System — это AI orchestration платформа для автоматического создания, обработки и публикации контента.

Основные компоненты:
Kernel — control plane (оркестрация и управление задачами)
Execution Layer — выполнение задач через LLM (локально / API)
Knowledge Layer (RAG) — работа с данными и памятью (в разработке)
Intelligence Layer — принятие решений (следующий этап)
🏗️ System Architecture
Layers
Data Flow
Target Architecture
Current State
⚙️ Core Modules
Kernel
Overview
Components
Flows
API
🔗 Contracts
Task
Context
Agent Result
📥 Pipelines
Ingestion Pipeline
Ingestion Status
📊 Current Status
Stage 4 — ✅ Completed
Kernel orchestration
Hybrid execution
Retry / fallback / timeout
Observability
Stage 5 — 🔄 In Progress
Knowledge Layer (RAG)
Agents Pipeline (MVP)
🧠 Next Stages
Intelligence Layer (decision making)
Human-in-the-loop
Automation (full cycle content generation)
📦 Internal Modules Documentation
Kernel:
../kernel/docs/README.md
📌 Principles
Modular architecture (agents-based)
Pipeline-driven execution
Separation of concerns
Scalable by design
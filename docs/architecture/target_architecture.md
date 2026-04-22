# AI Content Engine — Target Architecture

## Overview

Полная целевая архитектура системы AI Content Engine.

Система построена как modular monolith с возможностью перехода в distributed system.

---

## Layers

### 1. Infrastructure Layer
- Docker
- PostgreSQL
- Qdrant
- MinIO
- LLM backends

---

### 2. Kernel Layer
- Task Manager
- LLM Router
- Policy Engine
- Budget Controller
- Context Orchestrator

---

### 3. Context Layer
- Static Memory
- Dynamic Memory
- Semantic Memory (RAG)
- Summarized Memory

---

### 4. Agents Layer
- Analyzer
- Editor
- SEO
- Publisher
- QA

---

### 5. Workflow Layer
- orchestration logic
- transitions
- approval points

---

### 6. Projects Layer
- isolated environments
- budgets
- configs

---

### 7. Control Layer
- UI
- dashboards

---

### 8. Observability Layer
- logs
- metrics
- tracing

---

### 9. Versioning Layer
- prompts
- workflows
- configs

---

### 10. Human-in-the-loop Layer
- approvals
- overrides
- feedback

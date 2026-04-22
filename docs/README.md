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

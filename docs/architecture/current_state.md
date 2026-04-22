# Current System State — v0.4 (Kernel MVP)

## Implemented Layers

### API Layer
- FastAPI
- endpoint /task
- endpoint /health

---

### Kernel Layer (PARTIAL)

Implemented:
- TaskManager (FSM)
- Coordinator (orchestration)
- ContextBuilder
- ModelRouter (MVP)

Features:
- retry
- fallback (API → local)
- timeout
- concurrency limit
- queue (in-memory)

---

### Execution Layer

- Local executor (Ollama)
- API executor (OpenAI)

---

### Observability (PARTIAL)

- logging
- tracing
- metrics (in-memory)

---

## Not Implemented Yet

- Context Layer (RAG)
- Agents Layer
- Workflow Layer
- Projects Layer
- Versioning Layer
- Human-in-the-loop

---

## System Type

Current system is:

```text
AI execution kernel (orchestration engine)
Guarantees
 - system does not crash on failure
 - fallback always available
 - timeout protection
 - controlled concurrency
Limitations
 - no persistent storage
 - no circuit breaker
 - no rate limiting
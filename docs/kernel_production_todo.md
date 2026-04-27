# Kernel Production TODO

## Reliability
- Circuit breaker for API
- Retry policy tuning
- Executor health tracking

## Scaling
- Replace in-memory queue
- Add Redis / message broker

## Storage
- Persistent Task storage (PostgreSQL)

## Security
- Rate limiting
- Auth layer

## Observability
- Export metrics (Prometheus)
- Structured logging (JSON)

## Routing
- Replace heuristic router with classifier

# Kernel Production TODO

## Performance
- [ ] Cache embedding model (singleton)
- [ ] Add RAG toggle (dev mode)
- [ ] Optimize prompt size
- [ ] Introduce streaming by default

## Context Layer
- [ ] Structured knowledge context
- [ ] Memory system (session/user)
- [ ] Context enrichment pipeline

## Execution Layer
- [ ] Async execution
- [ ] Queue system
- [ ] Fallback strategies (API)

## Dev/Prod Modes
- [ ] Config-based mode switch
- [ ] Lightweight dev models
- [ ] Full models for production

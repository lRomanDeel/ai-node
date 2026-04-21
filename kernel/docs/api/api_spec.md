# Kernel API Specification

## POST /task

### Description

Создание и выполнение задачи.

---

### Request
POST /task

Body:
{
"input": "string"
}


---

### Response
{
"id": "string",
"status": "completed",
"result": "string"
}


---

## Future Endpoints

- GET /task/{id}
- GET /tasks
- POST /task/{id}/retry
- DELETE /task/{id}

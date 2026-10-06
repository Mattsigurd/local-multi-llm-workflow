# Architecture Plan: Priority and Due Date Support

## Overview

This repository uses a minimal FastAPI demo application as the shared baseline for comparing local multi-LLM workflow approaches. The requested feature adds `priority` and `due_date` support to each Todo item.

## Affected components

- `demo-project/app/main.py`: API model and endpoints
- `demo-project/tests/test_main.py`: validation of priority and due date behavior
- `workflows/crewai/config.py`: endpoint-to-role routing
- `workflows/crewai/agents.py`: local multi-agent orchestration
- `README.md`: user-facing workflow and setup documentation

## Responsibilities

### Data model

The Todo item model should store at least:

- `title`
- `description`
- `priority` with a constrained set such as `low | medium | high`
- `due_date` as a date-like string
- `completed`

### API layer

The API contract should expose the enriched Todo data in both create and read responses.

### Validation and quality

Tests should confirm:

- priority values are accepted in the allowed set
- due dates are serialized and returned correctly
- health and read flows remain stable

## Interface contracts

```python
class TodoItem(BaseModel):
    id: int | None = None
    title: str
    description: str | None = None
    priority: Literal["low", "medium", "high"] = "medium"
    due_date: str | None = None
    completed: bool = False
```

## Endpoint routing

The CrewAI workflow splits model usage by role:

- planning roles: `http://localhost:11434`
- coding/test roles: `http://localhost:11435`

This routing is centralized in `workflows/crewai/config.py` so it can be adjusted without changing the agent logic itself.

## Risks and constraints

- Local LLMs vary in output quality and may need prompt tightening.
- File editing should remain reviewable with Git diffs.
- The critical reliability issue is not model creativity but controlled tool usage and verification against real tests.

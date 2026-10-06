from __future__ import annotations

from typing import Literal

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="Todo API", version="0.1.0")

Priority = Literal["low", "medium", "high"]


class TodoItem(BaseModel):
    id: int | None = None
    title: str = Field(..., min_length=1)
    description: str | None = None
    priority: Priority = "medium"
    due_date: str | None = None
    completed: bool = False


TODOS: list[TodoItem] = [
    TodoItem(
        id=1,
        title="Draft the project overview",
        description="Summarize the assignment and workflow baseline.",
        priority="high",
        due_date="2026-10-08",
        completed=False,
    )
]


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/todos", response_model=list[TodoItem])
def list_todos() -> list[TodoItem]:
    return TODOS


@app.post("/todos", response_model=TodoItem, status_code=201)
def create_todo(item: TodoItem) -> TodoItem:
    next_id = max((todo.id or 0 for todo in TODOS), default=0) + 1
    todo = item.model_copy(update={"id": next_id})
    TODOS.append(todo)
    return todo


@app.get("/todos/{todo_id}", response_model=TodoItem)
def get_todo(todo_id: int) -> TodoItem:
    for todo in TODOS:
        if todo.id == todo_id:
            return todo
    raise HTTPException(status_code=404, detail="Todo not found")

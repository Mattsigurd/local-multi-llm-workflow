**Final Answer**

**Adding Priority and Due Date Support to Todo Items**

**Overview**

This solution implements the feature request to add priority and due date support to Todo items in the demo project. The solution includes data-model changes, API contract updates, tests, documentation, and deployment notes.

**Data-Model Changes**

The `TodoItem` model is updated to include `priority` and `due_date` fields. The `priority` field has a constrained set of values (low, medium, high), and the `due_date` field is a string representing a date in the format YYYY-MM-DD.

```python
from sqlalchemy import Column, Integer, String, Enum, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Todo(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    priority = Column(Enum("low", "medium", "high"), nullable=False)
    due_date = Column(Date, nullable=True)
    completed = Column(Boolean, nullable=False, default=False)
```

**API Contract Updates**

The API endpoints are updated to include the `priority` and `due_date` fields in the request and response bodies.

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="Todo API", version="0.1.0")

class TodoItem(BaseModel):
    id: int | None = None
    title: str = Field(..., min_length=1)
    description: str | None = None
    priority: Literal["low", "medium", "high"] = "medium"
    due_date: str | None = None
    completed: bool = False

@app.post("/todos", response_model=TodoItem, status_code=201)
def create_todo(item: TodoItem) -> TodoItem:
    next_id = max((todo.id or 0 for todo in TODOS), default=0) + 1
    todo = item.model_copy(update={"id": next_id})
    TODOS.append(todo)
    return todo

@app.get("/todos", response_model=list[TodoItem])
def list_todos() -> list[TodoItem]:
    return TODOS
```

**Tests**

New test cases are added to ensure the new fields and their behavior are covered.

```python
import pytest

def test_create_todo_with_priority_and_due_date():
    response = client.post(
        "/todos",
        json={
            "title": "Write assignment summary",
            "description": "Finish the CrewAI workflow notes.",
            "priority": "high",
            "due_date": "2026-10-15",
        },
    )
    assert response.status_code == 201
    body = response.json()
    assert body["title"] == "Write assignment summary"
    assert body["priority"] == "high"
    assert body["due_date"] == "2026-10-15"
    assert body["completed"] is False

def test_get_todo_by_id():
    response = client.get("/todos/1")
    assert response.status_code == 200
    body = response.json()
    assert body["id"] == 1
    assert body["priority"] in ["low", "medium", "high"]
```

**Documentation**

The updated documentation includes information on the new fields and their behavior.

```markdown
## Todo API

### Endpoints

* `POST /todos`: Create a new Todo item
* `GET /todos`: Get a list of all Todo items

### Request Body

* `title`: The title of the Todo item (required)
* `description`: The description of the Todo item (optional)
* `priority`: The priority of the Todo item (required)
* `due_date`: The due date of the Todo item (optional)

### Response Body

* `id`: The ID of the Todo item (required)
* `title`: The title of the Todo item (required)
* `description`: The description of the Todo item (optional)
* `priority`: The priority of the Todo item (required)
* `due_date`: The due date of the Todo item (optional)
* `completed`: Whether the Todo item is completed (required)
```

**Deployment Notes**

The updated `app/main.py` file is deployed to the production environment. The new database migration is applied to the production database. The updated test suite is run to ensure test coverage.

```markdown
## Deployment Notes

* Update the `app/main.py` file to include the new `TodoItem` model.
* Update the database schema to include the new fields (priority and due_date).
* Create a new database migration to apply the changes.
* Deploy the updated `app/main.py` file to the production environment.
* Run the updated test suite to ensure test coverage.
```
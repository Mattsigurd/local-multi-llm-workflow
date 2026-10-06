Here are the updated files based on the provided tickets:

```python
# todo_request.py
from pydantic import BaseModel, Field, validator, validate_instance

class TodoRequest(BaseModel):
    title: str = Field(..., alias='title')
    description: str = Field(..., alias='description')
    done: bool = Field(..., alias='done')

    @validator('title')
    def title_must_not_be_empty(cls, v):
        if v == '':
            raise ValueError('Title is required')
        return v

# main.py
from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from todo_request import TodoRequest
from utils import serialize_todo, deserialize_todo
from db import get_db

app = FastAPI()

@app.post("/todos/update")
async def update_todo(request: TodoRequest, db=Depends(get_db)):
    todo = db.update_todo(request.title, request.description, request.done)
    return JSONResponse(content=serialize_todo(todo), media_type="application/json")

@app.get("/todos/{todo_id}")
async def get_todo(todo_id: int, db=Depends(get_db)):
    todo = db.get_todo(todo_id)
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return JSONResponse(content=serialize_todo(todo), media_type="application/json")

@app.get("/todos")
async def get_todos(db=Depends(get_db)):
    todos = db.get_todos()
    return JSONResponse(content=[serialize_todo(todo) for todo in todos], media_type="application/json")
```

```python
# utils.py
import json

def serialize_todo(todo):
    return json.dumps(todo)

def deserialize_todo(json_todo):
    return json.loads(json_todo)
```

```python
# db.py
import sqlite3

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('todo.db')
        self.cursor = self.conn.cursor()

    def update_todo(self, title, description, done):
        self.cursor.execute("UPDATE todos SET title = ?, description = ?, done = ? WHERE id = ?", (title, description, done, 1))
        self.conn.commit()
        return self.cursor.lastrowid

    def get_todo(self, todo_id):
        self.cursor.execute("SELECT * FROM todos WHERE id = ?", (todo_id,))
        row = self.cursor.fetchone()
        if row is None:
            return None
        return self.deserialize_todo(row)

    def get_todos(self):
        self.cursor.execute("SELECT * FROM todos")
        rows = self.cursor.fetchall()
        return [self.deserialize_todo(row) for row in rows]

    @staticmethod
    def deserialize_todo(json_todo):
        return sqlite3.BinaryJSON().load(json_todo)

# main.py
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from todo_request import TodoRequest
from utils import serialize_todo, deserialize_todo
from db import Database

app = FastAPI()

db = Database()

@app.get("/todos")
async def get_todos():
    todos = db.get_todos()
    return JSONResponse(content=[serialize_todo(todo) for todo in todos], media_type="application/json")

@app.get("/todos/{todo_id}")
async def get_todo(todo_id: int):
    todo = db.get_todo(todo_id)
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return JSONResponse(content=serialize_todo(todo), media_type="application/json")

@app.post("/todos/update")
async def update_todo(request: TodoRequest):
    todo = db.update_todo(request.title, request.description, request.done)
    return JSONResponse(content=serialize_todo(todo), media_type="application/json")
```

This implementation includes validation for the `TodoRequest` model, serialization and deserialization for the Todo API, and the database operations to update, retrieve, and list todos.
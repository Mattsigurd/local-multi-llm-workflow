# Implementation Plan

Here's a short implementation plan for the task:

1. **Create the endpoint**: Add a new endpoint `/todos/{todo_id}` that takes the `todo_id` as a path parameter. This endpoint will be used to update an existing Todo.

    ```python
@app.put("/todos/{todo_id}", response_model=TodoItem)
```

2. **Extract the `todo_id`**: Extract the `todo_id` from the path parameter and use it to retrieve the Todo item that needs to be updated. This can be done by finding the Todo item with the matching `id` in the `TODOS` list.

    ```python
@app.put("/todos/{todo_id}", response_model=TodoItem)
def update_todo(todo_id: int, item: TodoItem) -> TodoItem:
    for todo in TODOS:
        if todo.id == todo_id:
            # ...
```

3. **Validate the request body**: Validate the request body to ensure it contains only the fields that need to be updated. For example, if the `priority` field is not provided in the request body, it should not be updated.

    ```python
@app.put("/todos/{todo_id}", response_model=TodoItem)
def update_todo(todo_id: int, item: TodoItem) -> TodoItem:
    for todo in TODOS:
        if todo.id == todo_id:
            # Validate item
            if todo.id != item.id or todo.title != item.title:
                raise HTTPException(status_code=400, detail="Invalid item")
            # ...
```

4. **Update the Todo item**: Update the existing Todo item with the new values from the request body. If a field is not provided in the request body, its value should be left unchanged.

    ```python
@app.put("/todos/{todo_id}", response_model=TodoItem)
def update_todo(todo_id: int, item: TodoItem) -> TodoItem:
    for todo in TODOS:
        if todo.id == todo_id:
            # Update item
            updated_item = item.model_copy(update={"id": todo.id})
            for field, value in item.dict().items():
                if field != "id" and value != todo[field]:
                    updated_item[field] = value
            TODOS[todo_id - 1] = updated_item
            return updated_item
    raise HTTPException(status_code=404, detail="Todo not found")
```

Note that the `id` field is used to uniquely identify the Todo item. If the `id` field is not unique, it should not be used as the primary key.
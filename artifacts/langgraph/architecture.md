# Architecture

Here are 3-5 short architecture points to add a PUT /todos/{todo_id} endpoint that updates an existing Todo:

1. **Endpoint Creation**: Add a new endpoint `/todos/{todo_id}` that takes the `todo_id` as a path parameter and returns the updated Todo item. This endpoint will be used to update an existing Todo.

2. **Parameter Extraction**: Extract the `todo_id` from the path parameter and use it to retrieve the Todo item that needs to be updated.

3. **Validation**: Validate the request body to ensure it contains only the fields that need to be updated. For example, if the `priority` field is not provided in the request body, it should not be updated.

4. **Update Logic**: Update the existing Todo item with the new values from the request body. If a field is not provided in the request body, its value should be left unchanged.

5. **Status Code**: Return a 200 OK status code to indicate that the update was successful, and include the updated Todo item in the response body.

Here is an example of how the updated code could look like:
```
@app.put("/todos/{todo_id}", response_model=TodoItem)
def update_todo(todo_id: int, item: TodoItem) -> TodoItem:
    for todo in TODOS:
        if todo.id == todo_id:
            updated_item = item.model_copy(update={"id": todo.id})
            for field, value in item.dict().items():
                if field != "id" and value != todo[field]:
                    updated_item[field] = value
            TODOS[todo_id - 1] = updated_item
            return updated_item
    raise HTTPException(status_code=404, detail="Todo not found")
```
Note that this implementation assumes that the `id` field is unique for each Todo item. If this is not the case, the `id` field should be excluded from the `model_copy` method.
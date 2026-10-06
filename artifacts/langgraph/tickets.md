# Development Tickets

Here are the two small tickets:

**Ticket 1: Create the endpoint**

* Title: Create endpoint for updating Todo items
* Scope: Implement the `/todos/{todo_id}` endpoint that takes the `todo_id` as a path parameter
* Acceptance Criteria:
 + The endpoint is created at the correct URL (`/todos/{todo_id}`)
 + The endpoint returns a 200 OK response with the updated Todo item
 + The endpoint returns a 404 status code if the Todo item is not found
* Dependencies:
 + `TODOS` list is available
* Definition of Done:
 + The endpoint is implemented and tested successfully
 + The endpoint returns the expected response with the updated Todo item

**Ticket 2: Update the Todo item**

* Title: Update Todo item with new values
* Scope: Implement the logic to update the existing Todo item with the new values from the request body
* Acceptance Criteria:
 + The updated Todo item is correctly updated with the new values
 + The updated Todo item is returned in the response with a 200 OK status code
 + The updated Todo item is stored in the `TODOS` list
 + The endpoint returns a 400 status code if the request body is invalid
* Dependencies:
 + `update_todo` endpoint is implemented and tested successfully
 + `TODOS` list is available
* Definition of Done:
 + The logic to update the Todo item is implemented and tested successfully
 + The updated Todo item is correctly returned in the response with a 200 OK status code
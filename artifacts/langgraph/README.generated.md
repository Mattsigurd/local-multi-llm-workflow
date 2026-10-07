# Todo API

**Documentation for Demo Project**

**Setup and Run Instructions**

1. Clone the repository: `git clone https://github.com/paulsebastiankrus/assignment1.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Run the application: `python main.py`

**API Usage**

### Get Health

* URL: `/health`
* Method: `GET`
* Response: `200 OK` with JSON body `{ "status": "ok" }`

### List Todos

* URL: `/todos`
* Method: `GET`
* Response: List of Todo items

### Create Todo

* URL: `/todos`
* Method: `POST`
* Request Body: `TodoItem` object
* Response: Created Todo item

### Get Todo

* URL: `/todos/{todo_id}`
* Method: `GET`
* Path Parameter: `todo_id` (integer)
* Response: Todo item

### Update Todo

* URL: `/todos/{todo_id}`
* Method: `PUT`
* Path Parameter: `todo_id` (integer)
* Request Body: `TodoItem` object
* Response: Updated Todo item

**Basic Operational Notes**

* The Todo data is stored in memory and is lost when the application restarts.
* The application uses FastAPI and Pydantic for building and validating the Todo API.
* The `TODOS` list stores all Todo items, which are retrieved and updated using their unique `id` field.
* The `update_todo` endpoint updates an existing Todo item with the new values from the request body.
* The application raises an `HTTPException` with a 404 status code if the Todo item is not found.
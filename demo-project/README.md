# Todo API

**Documentation for Demo Project**

**Setup and Run Instructions**

1. Install the required dependencies by running `pip install -r requirements.txt` in the project directory.
2. Start the application by running `uvicorn app.main:app --host 0.0.0.0 --port 8000` in the terminal.
3. Test the application by running `pytest` in the terminal.

**API Usage**

### Health Endpoint

* URL: `http://localhost:8000/health`
* Method: GET
* Response: A JSON object with a single key-value pair: `{"status": "ok"}`

### Todo Endpoints

#### List Todos

* URL: `http://localhost:8000/todos`
* Method: GET
* Response: A JSON list of Todo objects

#### Create Todo

* URL: `http://localhost:8000/todos`
* Method: POST
* Request Body: A JSON object with the following keys:
	+ `title`: string
	+ `description`: string
	+ `priority`: string (one of "low", "medium", or "high")
	+ `due_date`: string (optional)
	+ `completed`: boolean (optional)
* Response: A JSON object with the created Todo object

#### Get Todo

* URL: `http://localhost:8000/todos/{todo_id}`
* Method: GET
* Path Parameter: `todo_id` (integer)
* Response: A JSON object with the Todo object

#### Update Todo

* URL: `http://localhost:8000/todos/{todo_id}`
* Method: PUT
* Path Parameter: `todo_id` (integer)
* Request Body: A JSON object with the following keys:
	+ `title`: string
	+ `description`: string
	+ `priority`: string (one of "low", "medium", or "high")
	+ `due_date`: string (optional)
	+ `completed`: boolean (optional)
* Response: A JSON object with the updated Todo object

**Basic Operational Notes**

* The Todo data is stored in memory and is lost when the application restarts.
* The application uses a simple validation mechanism to ensure that the request body contains the expected fields.
* The application returns a 400 Bad Request error if the request body is invalid.
* The application returns a 404 Not Found error if the Todo object with the given ID is not found.
* The application uses the `model_copy` method to update the Todo object, which creates a new copy of the object with the updated values.

**Known Limitations and Risks**

* The Todo data is stored in memory and is lost when the application restarts.
* AI-generated code may require human review before being applied.
* The local LLM endpoints are intended to remain local and should not be exposed publicly without authentication and appropriate security controls.
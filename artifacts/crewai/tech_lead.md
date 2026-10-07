**Task Breakdown: Adding Priority and Due Date Support to Todo Items**

**Task 1: Update Data Model**

* Update the `TodoItem` model to include `priority` and `due_date` fields.
* Ensure `priority` is a string with a constrained set of values (`low`, `medium`, `high`).
* Ensure `due_date` is a string in YYYY-MM-DD format.
* Update the `TODOS` list to include Todo items with the new `priority` and `due_date` fields.

**Task 2: Update API Contract**

* Update the `POST /todos` endpoint to include `priority` and `due_date` fields in the request body.
* Update the `GET /todos` endpoint to include `priority` and `due_date` fields in the response body.
* Update the `GET /todos/{todo_id}` endpoint to include `priority` and `due_date` fields in the response body.

**Task 3: Implement Priority and Due Date Validation**

* Implement a validation check in the `create_todo` function to ensure `priority` and `due_date` fields are in the correct format.
* Update the `get_todo` function to include the `priority` and `due_date` fields in the response body.

**Task 4: Update Tests**

* Update the `app/tests/test_main.py` file to include new tests for creating and retrieving Todo items with `priority` and `due_date`.
* Update the existing tests to include the new `priority` and `due_date` fields in the request and response bodies.

**Task 5: Update Documentation**

* Update the documentation to include information about the new `priority` and `due_date` fields, including their format and validation rules.
* Update the documentation to include examples of how to use the new fields in the API requests and responses.

**Task 6: Update Deployment Notes**

* Update the deployment notes to include the updated `app/main.py` and `app/tests/test_main.py` files.
* Update the database to include the new `priority` and `due_date` fields.

**Task 7: Review and Test**

* Review the updated code to ensure all tasks have been completed correctly.
* Test the API endpoints to ensure `priority` and `due_date` fields are being validated and returned correctly.

**Acceptance Criteria**

* The `priority` and `due_date` fields are included in the response body for all API endpoints.
* The `create_todo` function validates the `priority` and `due_date` fields correctly.
* The `get_todo` function returns the `priority` and `due_date` fields correctly.
* The tests pass for all API endpoints.

**Definition of Done**

* The updated code has been reviewed and tested to ensure all tasks have been completed correctly.
* The API endpoints are functioning as expected with `priority` and `due_date` fields.
* The documentation is up-to-date and includes information about the new fields.
* The deployment notes are accurate and include the updated files.
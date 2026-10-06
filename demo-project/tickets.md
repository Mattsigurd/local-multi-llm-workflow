# Development Tickets

Here are the two small tickets based on the implementation plan:

**Ticket 1: Update Todo Model**

* **Title:** Update Todo Model to include an `update` field
* **Scope:** Update the Todo model to include an `update` field that can be used to override the values of existing fields.
* **Acceptance Criteria:**
	+ The Todo model includes an `update` field with a type of `dict[str, str] = {}`
	+ The `update` field allows the client to only update specific fields without having to recreate the entire Todo object
* **Dependencies:**
	+ None
* **Definition of Done:** The updated Todo model has been applied, and all relevant code has been updated to reflect the changes.

**Ticket 2: Implement Validation and Error Handling for Todo Updates**

* **Title:** Implement validation and error handling for Todo updates
* **Scope:** Implement validation and error handling logic to ensure that the incoming request body contains the expected fields and that the validation errors are returned with a 400 Bad Request error.
* **Acceptance Criteria:**
	+ The `update_todo` function validates the incoming request body and returns a 400 Bad Request error if any validation errors occur
	+ The `update_todo` function returns the updated Todo object in the response body if validation succeeds
* **Dependencies:**
	+ Ticket 1: The updated Todo model is in place
	+ `validate_todo_item` function is implemented and available for use
* **Definition of Done:** The `update_todo` function has been updated to include validation and error handling logic, and all relevant tests have been written to ensure the functionality is working as expected.
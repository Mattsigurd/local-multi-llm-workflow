from __future__ import annotations

from crewai import Task

DEFAULT_FEATURE_REQUEST = (
    "Add priority and due_date support to Todo items in the demo project. "
    "Update the data model, API contract, tests, documentation, and deployment notes."
)


def build_tasks(agents: dict[str, object], feature_request: str | None = None) -> dict[str, Task]:
    request = feature_request or DEFAULT_FEATURE_REQUEST

    return {
        "architecture": Task(
            description=(
                "Review the repository and the feature request. Produce a concise architecture plan "
                "that identifies affected modules, data-model changes, API impacts, and implementation boundaries. "
                f"Feature request: {request}"
            ),
            agent=agents["architect"],
            expected_output="A markdown-style architecture document describing components, interfaces, and design decisions.",
        ),
        "tech_lead": Task(
            description=(
                "Use the architecture plan to create a structured set of implementation tasks. "
                "Include dependencies, acceptance criteria, and a simple split between developer workstreams. "
                f"Feature request: {request}"
            ),
            agent=agents["tech_lead"],
            expected_output="A JSON-like or markdown task breakdown with dependency ordering and definition of done.",
        ),
        "developer_1": Task(
            description=(
                "Implement the model and data-layer changes needed for the feature. Handle domain fields, validation, "
                "and any persistence or schema updates required to support the request. "
                f"Feature request: {request}"
            ),
            agent=agents["developer_1"],
            expected_output="Implementation notes plus a concrete set of code-level changes for the model and repository layer.",
        ),
        "developer_2": Task(
            description=(
                "Implement the API and integration changes required by the feature request. Update endpoint contracts, "
                "request validation, and response payload handling so the feature works end-to-end. "
                f"Feature request: {request}"
            ),
            agent=agents["developer_2"],
            expected_output="Implementation notes plus a concrete set of code-level changes for the API layer and business logic.",
        ),
        "tester": Task(
            description=(
                "Review the implementation and add or update real tests to validate behaviour. Run the relevant test "
                "command, confirm the feature passes, and report any failures. "
                f"Feature request: {request}"
            ),
            agent=agents["tester"],
            expected_output="A real validation report with tested scenarios, commands run, and pass/fail evidence.",
        ),
        "documentation": Task(
            description=(
                "Update docs and operational notes so the feature is traceable and understandable. Capture the user-visible "
                "contract and any deployment or maintenance guidance. "
                f"Feature request: {request}"
            ),
            agent=agents["documentation"],
            expected_output="A concise documentation update summarizing the feature, interface changes, and user guidance.",
        ),
        "deployment": Task(
            description=(
                "Check that the repository can be deployed or validated locally after the feature is implemented. "
                "Summarize release readiness, operational dependencies, and any follow-up actions. "
                f"Feature request: {request}"
            ),
            agent=agents["deployment"],
            expected_output="A deployment-readiness summary with checks, risks, and an explicit go/no-go recommendation.",
        ),
    }

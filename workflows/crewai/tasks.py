from __future__ import annotations

from pathlib import Path

from crewai import Task

DEFAULT_FEATURE_REQUEST = (
    "Add priority and due_date support to Todo items in the demo project. "
    "Update the data model, API contract, tests, documentation, and deployment notes."
)

ROOT = Path(__file__).resolve().parents[2]


def _artifact_context(*relative_paths: str, limit: int = 2500) -> str:
    sections = []
    for relative_path in relative_paths:
        path = ROOT / relative_path
        if path.exists():
            content = path.read_text(encoding="utf-8")[:limit]
            sections.append(f"--- {relative_path} ---\n{content}")
        else:
            sections.append(f"--- {relative_path} ---\nNot generated yet.")
    return "\n\n".join(sections)


def build_tasks(agents: dict[str, object], feature_request: str | None = None) -> dict[str, Task]:
    request = feature_request or DEFAULT_FEATURE_REQUEST
    architecture_context = _artifact_context("artifacts/architecture.md")
    planning_context = _artifact_context("artifacts/tasks.json", limit=1800)
    repository_context = _artifact_context(
        "demo-project/app/main.py",
        "demo-project/tests/test_main.py",
        limit=3000,
    )

    return {
        "architecture": Task(
            description=(
                "Review the repository and the feature request. Produce a concise architecture plan "
                "that identifies affected modules, data-model changes, API impacts, and implementation boundaries. "
                "Use only the existing Python/FastAPI project shown below. Do not invent languages, databases, "
                "services, modules, or endpoints that are not justified by the request. Clearly label proposals "
                "as recommendations; do not claim that code was changed. Return no more than 500 words. "
                f"Feature request: {request}\n\nRepository context:\n{repository_context}"
            ),
            agent=agents["architect"],
            expected_output="A markdown-style architecture document describing components, interfaces, and design decisions.",
        ),
        "tech_lead": Task(
            description=(
                "Use the architecture plan to create a structured set of implementation tasks. "
                "Include dependencies, acceptance criteria, and a simple split between developer workstreams. "
                "Keep the tasks aligned with the existing Python/FastAPI files and do not introduce TypeScript, "
                "databases, or new services unless the request explicitly requires them. "
                f"Feature request: {request}\n\nExisting artifact context:\n{architecture_context}\n\n"
                f"Repository context:\n{repository_context}"
            ),
            agent=agents["tech_lead"],
            expected_output="A JSON-like or markdown task breakdown with dependency ordering and definition of done.",
        ),
        "developer_1": Task(
            description=(
                "Implement the model and data-layer changes needed for the feature. Handle domain fields, validation, "
                "and any persistence or schema updates required to support the request. "
                "This workflow currently has no file-editing tools, so return a reviewable patch proposal and do not "
                "claim that files were changed. Use only the existing Python/FastAPI project. "
                f"Feature request: {request}\n\nHandoff context:\n{planning_context}"
            ),
            agent=agents["developer_1"],
            expected_output="Implementation notes plus a concrete set of code-level changes for the model and repository layer.",
        ),
        "developer_2": Task(
            description=(
                "Implement the API and integration changes required by the feature request. Update endpoint contracts, "
                "request validation, and response payload handling so the feature works end-to-end. "
                "This workflow currently has no file-editing tools, so return a reviewable patch proposal and do not "
                "claim that files were changed. Use only the existing Python/FastAPI project. "
                f"Feature request: {request}\n\nHandoff context:\n{planning_context}"
            ),
            agent=agents["developer_2"],
            expected_output="Implementation notes plus a concrete set of code-level changes for the API layer and business logic.",
        ),
        "implementation": Task(
            description=(
                "Apply the already approved feature request to the existing repository. First read the current "
                "application and tests with the repository tools. Then use write_repository_file to apply only the "
                "necessary changes to the FastAPI project. Do not invent databases, services, languages, or files. "
                "Use paths such as demo-project/app/main.py or app/main.py for application files and "
                "demo-project/tests/test_main.py or tests/test_main.py for tests. "
                "Run the available tests after editing and report exactly which files were changed. "
                f"Feature request: {request}\n\nDeveloper proposals:\n"
                f"{_artifact_context('artifacts/crewai/developer_1.md', 'artifacts/crewai/developer_2.md')}"
            ),
            agent=agents["implementer"],
            expected_output="A concise record of files actually changed and the test command result.",
        ),
        "tester": Task(
            description=(
                "Review the implementation and add or update real tests to validate behaviour. Run the relevant test "
                "command, confirm the feature passes, and report any failures. "
                f"Feature request: {request}\n\nHandoff context:\n{planning_context}"
            ),
            agent=agents["tester"],
            expected_output="A real validation report with tested scenarios, commands run, and pass/fail evidence.",
        ),
        "documentation": Task(
            description=(
                "Update docs and operational notes so the feature is traceable and understandable. Capture the user-visible "
                "contract and any deployment or maintenance guidance. "
                f"Feature request: {request}\n\nHandoff context:\n{planning_context}"
            ),
            agent=agents["documentation"],
            expected_output="A concise documentation update summarizing the feature, interface changes, and user guidance.",
        ),
        "deployment": Task(
            description=(
                "Check that the repository can be deployed or validated locally after the feature is implemented. "
                "Summarize release readiness, operational dependencies, and any follow-up actions. "
                f"Feature request: {request}\n\nHandoff context:\n{planning_context}"
            ),
            agent=agents["deployment"],
            expected_output="A deployment-readiness summary with checks, risks, and an explicit go/no-go recommendation.",
        ),
    }

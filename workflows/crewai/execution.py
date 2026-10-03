from __future__ import annotations

import json
from pathlib import Path

DEFAULT_FEATURE_REQUEST = (
    "Add priority and due_date support to Todo items in the demo project. "
    "Update the data model, API contract, tests, documentation, and deployment notes."
)


def build_execution_plan(feature_request: str | None = None) -> dict[str, object]:
    request = feature_request or DEFAULT_FEATURE_REQUEST
    return {
        "status": "ready",
        "feature_request": request,
        "stages": [
            "architecture",
            "developer",
            "tester",
            "deployment",
        ],
        "validation_commands": [
            "pytest demo-project/tests -q",
        ],
        "artifacts": [
            "artifacts/architecture.md",
            "artifacts/tasks.json",
            "artifacts/execution_plan.json",
        ],
        "next_steps": [
            "Review the architecture plan and confirm scope.",
            "Split the feature into developer workstreams.",
            "Run the validation suite before shipping.",
        ],
    }


def persist_execution_plan(feature_request: str | None = None) -> dict[str, object]:
    root = Path(__file__).resolve().parents[2]
    artifacts_dir = root / "artifacts"
    artifacts_dir.mkdir(exist_ok=True)

    plan = build_execution_plan(feature_request)
    output_path = artifacts_dir / "execution_plan.json"
    output_path.write_text(json.dumps(plan, indent=2), encoding="utf-8")
    return plan

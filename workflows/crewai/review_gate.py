from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def build_review_gate(feature_request: str | None = None) -> dict[str, object]:
    request = feature_request or "Add priority and due_date support to Todo items in the demo project."
    return {
        "status": "pending_review",
        "feature_request": request,
        "plan": [
            "Review affected files and API contract.",
            "Implement model and endpoint updates.",
            "Run pytest and record the outcome.",
            "Summarize remaining risks or follow-ups.",
        ],
        "diff_preview": {
            "files": [
                "demo-project/app/main.py",
                "demo-project/tests/test_main.py",
                "README.md",
            ],
            "summary": "Adds priority and due_date fields with validation and document updates; no DB or external service changes required for this demo.",
        },
        "approval_required": True,
        "next_action": "Human review required before execution is approved.",
    }


def persist_review_gate(feature_request: str | None = None) -> dict[str, object]:
    gate = build_review_gate(feature_request)
    artifact_dir = ROOT / "artifacts"
    artifact_dir.mkdir(exist_ok=True)
    path = artifact_dir / "review_gate.json"
    path.write_text(json.dumps(gate, indent=2), encoding="utf-8")
    return gate

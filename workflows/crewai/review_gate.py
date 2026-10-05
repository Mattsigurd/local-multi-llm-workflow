from __future__ import annotations

import json
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REVIEW_GATE_PATH = ROOT / "artifacts" / "review_gate.json"


def _request_id(feature_request: str) -> str:
    return hashlib.sha256(feature_request.encode("utf-8")).hexdigest()[:12]


def build_review_gate(feature_request: str | None = None) -> dict[str, object]:
    request = feature_request or "Add priority and due_date support to Todo items in the demo project."
    return {
        "status": "pending_review",
        "feature_request": request,
        "request_id": _request_id(request),
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
    REVIEW_GATE_PATH.write_text(json.dumps(gate, indent=2), encoding="utf-8")
    return gate


def approve_review_gate(feature_request: str | None = None) -> dict[str, object]:
    request = feature_request or "Add priority and due_date support to Todo items in the demo project."
    if not REVIEW_GATE_PATH.exists():
        raise RuntimeError("No review gate exists. Create one with --review before approving it.")

    gate = json.loads(REVIEW_GATE_PATH.read_text(encoding="utf-8"))
    if gate.get("request_id") != _request_id(request):
        raise RuntimeError("The feature request does not match the pending review gate.")

    gate["status"] = "approved"
    gate["approval_required"] = False
    gate["next_action"] = "Execution approved."
    REVIEW_GATE_PATH.write_text(json.dumps(gate, indent=2), encoding="utf-8")
    return gate


def require_approved_review_gate(feature_request: str | None = None) -> None:
    request = feature_request or "Add priority and due_date support to Todo items in the demo project."
    if not REVIEW_GATE_PATH.exists():
        raise RuntimeError("Execution is blocked: create and approve a review gate first.")

    gate = json.loads(REVIEW_GATE_PATH.read_text(encoding="utf-8"))
    if gate.get("status") != "approved" or gate.get("request_id") != _request_id(request):
        raise RuntimeError("Execution is blocked: the matching review gate is not approved.")

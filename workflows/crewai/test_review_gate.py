from __future__ import annotations

from workflows.crewai.review_gate import build_review_gate


def test_review_gate_requires_human_approval() -> None:
    gate = build_review_gate("Add priority and due_date support to Todo items.")

    assert gate["status"] == "pending_review"
    assert gate["approval_required"] is True
    assert len(gate["plan"]) >= 3
    assert "diff_preview" in gate

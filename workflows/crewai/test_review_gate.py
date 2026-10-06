from __future__ import annotations

import pytest

import workflows.crewai.review_gate as review_gate
from workflows.crewai.review_gate import build_review_gate


def test_review_gate_requires_human_approval() -> None:
    gate = build_review_gate("Add priority and due_date support to Todo items.")

    assert gate["status"] == "pending_review"
    assert gate["approval_required"] is True
    assert len(gate["plan"]) >= 3
    assert "diff_preview" in gate


def test_execution_requires_matching_approved_gate(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(review_gate, "REVIEW_GATE_PATH", tmp_path / "review_gate.json")
    request = "Add labels to Todo items."

    review_gate.persist_review_gate(request)
    with pytest.raises(RuntimeError, match="not approved"):
        review_gate.require_approved_review_gate(request)

    review_gate.approve_review_gate(request)
    review_gate.require_approved_review_gate(request)


def test_approval_cannot_be_reused_for_another_request(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(review_gate, "REVIEW_GATE_PATH", tmp_path / "review_gate.json")
    review_gate.persist_review_gate("Add labels to Todo items.")

    with pytest.raises(RuntimeError, match="does not match"):
        review_gate.approve_review_gate("Add tags to Todo items.")

from __future__ import annotations

from workflows.crewai.execution import build_execution_plan


def test_build_execution_plan_has_stages_and_validation() -> None:
    plan = build_execution_plan("Add priority and due_date support to Todo items.")

    assert plan["status"] == "ready"
    assert "architecture" in plan["stages"]
    assert "developer" in plan["stages"]
    assert "tester" in plan["stages"]
    assert "deployment" in plan["stages"]
    assert "pytest" in plan["validation_commands"][0]

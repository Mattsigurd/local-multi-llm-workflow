from __future__ import annotations

from workflows.crewai.implementation_loop import execute_feature_cycle


def test_execute_feature_cycle_reports_success() -> None:
    report = execute_feature_cycle("Add priority and due_date support to Todo items.")

    assert report["done"] is True
    assert report["feature_status"]["status"] == "satisfied"
    assert report["validation"]["passed"] is True
    assert report["run_id"]
    assert report["validation"]["static_check"]["passed"] is True
    assert report["git_evidence"]["status_command_succeeded"] is True
    assert report["limitations"]

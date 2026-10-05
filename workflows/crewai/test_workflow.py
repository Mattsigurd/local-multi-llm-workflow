from __future__ import annotations

from workflows.crewai.agents import build_agents
from workflows.crewai.tasks import build_tasks


def test_build_tasks_cover_full_delivery_pipeline() -> None:
    tasks = build_tasks(build_agents())

    required = {
        "architecture",
        "tech_lead",
        "developer_1",
        "developer_2",
        "tester",
        "documentation",
        "deployment",
    }

    assert required.issubset(tasks)
    for task_name, task in tasks.items():
        assert task.description
        assert task.expected_output
        assert "priority" in task.description.lower() or task_name == "deployment"

    assert "Handoff context" in tasks["developer_1"].description
    assert "Existing artifact context" in tasks["tech_lead"].description

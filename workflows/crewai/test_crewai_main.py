from types import SimpleNamespace

import pytest

import workflows.crewai.main as workflow_main


class FakeCrew:
    def __init__(self, error: Exception | None = None) -> None:
        self.error = error

    def kickoff(self) -> str:
        if self.error:
            raise self.error
        return "completed"


def test_kickoff_persists_completed_task_outputs(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(workflow_main, "CREWAI_ARTIFACT_DIR", tmp_path)
    tasks = {"architecture": SimpleNamespace(output=SimpleNamespace(raw="plan"))}

    result = workflow_main.kickoff_and_persist(FakeCrew(), tasks, "feature")

    assert result == "completed"
    assert (tmp_path / "architecture.md").read_text(encoding="utf-8") == "plan"
    status = (tmp_path / "run_status.json").read_text(encoding="utf-8")
    assert '"status": "completed"' in status
    assert "architecture" in status


def test_kickoff_persists_failure_and_completed_outputs(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(workflow_main, "CREWAI_ARTIFACT_DIR", tmp_path)
    tasks = {"architecture": SimpleNamespace(output=SimpleNamespace(raw="plan"))}

    with pytest.raises(RuntimeError, match="model unavailable"):
        workflow_main.kickoff_and_persist(
            FakeCrew(RuntimeError("model unavailable")), tasks, "feature"
        )

    status = (tmp_path / "run_status.json").read_text(encoding="utf-8")
    assert '"status": "failed"' in status
    assert "model unavailable" in status
    assert (tmp_path / "architecture.md").exists()

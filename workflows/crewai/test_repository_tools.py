from pathlib import Path

import pytest

import workflows.crewai.repository_tools as repository_tools


def test_project_relative_app_path_is_mapped_to_demo_project() -> None:
    target = repository_tools._safe_path("app/main.py")

    assert target == repository_tools.ROOT / "demo-project" / "app" / "main.py"


def test_write_tool_accepts_project_relative_path(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(
        repository_tools,
        "ALLOWED_ROOTS",
        (tmp_path / "demo-project", tmp_path / "artifacts" / "crewai"),
    )
    monkeypatch.setattr(repository_tools, "ROOT", tmp_path)
    tool = repository_tools.WriteRepositoryFileTool()

    result = tool._run("app/generated.py", "value = 1\n")

    assert result == "Applied file change: demo-project/app/generated.py"
    assert (tmp_path / "demo-project" / "app" / "generated.py").read_text() == "value = 1\n"


def test_path_traversal_is_rejected() -> None:
    with pytest.raises(ValueError, match="outside"):
        repository_tools._safe_path("app/../../workflows/crewai/main.py")


def test_serialized_write_request_is_applied_after_approval(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(
        repository_tools,
        "ALLOWED_ROOTS",
        (tmp_path / "demo-project", tmp_path / "artifacts" / "crewai"),
    )
    monkeypatch.setattr(repository_tools, "ROOT", tmp_path)
    request = (
        '{"name":"write_repository_file","parameters":'
        '{"path":"app/generated.py","content":"value = 2\\n"}}'
    )

    applied = repository_tools.apply_serialized_write_requests(request)

    assert applied == ["Applied file change: demo-project/app/generated.py"]
    assert (tmp_path / "demo-project" / "app" / "generated.py").read_text() == "value = 2\n"
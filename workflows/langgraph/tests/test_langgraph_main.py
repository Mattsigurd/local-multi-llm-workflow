from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from main import PROJECT_DIR, local_endpoint, route_after_tests


def test_project_directory_is_repository_relative() -> None:
    assert PROJECT_DIR.name == "demo-project"
    assert (PROJECT_DIR / "app" / "main.py").exists()


def test_only_local_model_endpoints_are_allowed() -> None:
    assert local_endpoint("TEST_ENDPOINT", "http://localhost:11434") == "http://localhost:11434"

    with pytest.raises(ValueError, match="must point to a local endpoint"):
        local_endpoint("TEST_ENDPOINT", "https://example.com")


def test_failed_quality_gate_stops_downstream_work() -> None:
    assert route_after_tests({"test_passed": True}) == "passed"
    assert route_after_tests({"test_passed": False}) == "failed"

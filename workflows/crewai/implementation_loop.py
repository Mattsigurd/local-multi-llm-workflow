from __future__ import annotations

import json
import hashlib
import subprocess
from pathlib import Path

from workflows.crewai.execution import persist_execution_plan

ROOT = Path(__file__).resolve().parents[2]
APP_PATH = ROOT / "demo-project" / "app" / "main.py"


def _run_id(feature_request: str) -> str:
    return hashlib.sha256(feature_request.encode("utf-8")).hexdigest()[:12]


def ensure_demo_feature_support() -> dict[str, object]:
    source = APP_PATH.read_text(encoding="utf-8")
    required = ["priority: Priority = \"medium\"", "due_date: str | None = None"]
    present = all(token in source for token in required)
    return {
        "status": "satisfied" if present else "missing",
        "feature_checks": {
            "priority_field_present": "priority: Priority = \"medium\"" in source,
            "due_date_field_present": "due_date: str | None = None" in source,
        },
        "file": str(APP_PATH.relative_to(ROOT)),
    }


def run_validation() -> dict[str, object]:
    test_result = subprocess.run(
        [".venv/bin/python", "-m", "pytest", "demo-project/tests", "-q"],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    static_result = subprocess.run(
        [".venv/bin/python", "-m", "compileall", "-q", "demo-project", "workflows"],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    return {
        "exit_code": test_result.returncode,
        "passed": test_result.returncode == 0 and static_result.returncode == 0,
        "stdout": test_result.stdout.strip(),
        "stderr": test_result.stderr.strip(),
        "static_check": {
            "command": ".venv/bin/python -m compileall -q demo-project workflows",
            "passed": static_result.returncode == 0,
            "stderr": static_result.stderr.strip(),
        },
    }


def collect_git_evidence() -> dict[str, object]:
    status = subprocess.run(
        ["git", "status", "--short"], cwd=str(ROOT), capture_output=True, text=True
    )
    diff_stat = subprocess.run(
        ["git", "diff", "--stat"], cwd=str(ROOT), capture_output=True, text=True
    )
    return {
        "status": status.stdout.strip(),
        "diff_stat": diff_stat.stdout.strip(),
        "status_command_succeeded": status.returncode == 0,
        "diff_command_succeeded": diff_stat.returncode == 0,
    }


def execute_feature_cycle(feature_request: str | None = None) -> dict[str, object]:
    request = feature_request or "Add priority and due_date support to Todo items."
    plan = persist_execution_plan(request)
    feature_status = ensure_demo_feature_support()
    validation = run_validation()
    report = {
        "run_id": _run_id(request),
        "execution_plan": plan,
        "feature_status": feature_status,
        "validation": validation,
        "git_evidence": collect_git_evidence(),
        "limitations": [
            "The feature check verifies the expected model fields but does not replace API behavior tests.",
            "Git evidence is recorded for review; the workflow does not create commits automatically.",
        ],
        "done": feature_status["status"] == "satisfied" and validation["passed"],
    }

    output_path = ROOT / "artifacts" / "implementation_status.json"
    output_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report

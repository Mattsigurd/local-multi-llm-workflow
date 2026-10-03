from __future__ import annotations

import json
import subprocess
from pathlib import Path

from workflows.crewai.execution import persist_execution_plan

ROOT = Path(__file__).resolve().parents[2]
APP_PATH = ROOT / "demo-project" / "app" / "main.py"


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
    result = subprocess.run(
        [".venv/bin/python", "-m", "pytest", "demo-project/tests", "-q"],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    return {
        "exit_code": result.returncode,
        "passed": result.returncode == 0,
        "stdout": result.stdout.strip(),
        "stderr": result.stderr.strip(),
    }


def execute_feature_cycle(feature_request: str | None = None) -> dict[str, object]:
    plan = persist_execution_plan(feature_request)
    feature_status = ensure_demo_feature_support()
    validation = run_validation()
    report = {
        "execution_plan": plan,
        "feature_status": feature_status,
        "validation": validation,
        "done": feature_status["status"] == "satisfied" and validation["passed"],
    }

    output_path = ROOT / "artifacts" / "implementation_status.json"
    output_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report

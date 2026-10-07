from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CREWAI_ARTIFACT_DIR = ROOT / "artifacts" / "crewai"


def persist_task_outputs(tasks: dict[str, object]) -> list[str]:
    CREWAI_ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    completed = []
    for task_name, task in tasks.items():
        output = getattr(task, "output", None)
        raw_output = getattr(output, "raw", None) if output is not None else None
        if not raw_output:
            continue
        (CREWAI_ARTIFACT_DIR / f"{task_name}.md").write_text(str(raw_output), encoding="utf-8")
        completed.append(task_name)
    return completed


def persist_run_status(
    feature_request: str | None,
    status: str,
    completed_tasks: list[str],
    error: str | None = None,
) -> None:
    CREWAI_ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    report = {
        "status": status,
        "feature_request": feature_request,
        "completed_tasks": completed_tasks,
    }
    if error:
        report["error"] = error
    (CREWAI_ARTIFACT_DIR / "run_status.json").write_text(
        json.dumps(report, indent=2), encoding="utf-8"
    )


def kickoff_and_persist(crew: Crew, tasks: dict[str, object], feature_request: str | None) -> str:
    try:
        result = crew.kickoff()
    except Exception as error:
        completed_tasks = persist_task_outputs(tasks)
        persist_run_status(feature_request, "failed", completed_tasks, str(error))
        raise

    completed_tasks = persist_task_outputs(tasks)
    persist_run_status(feature_request, "completed", completed_tasks)
    return str(result)
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from crewai import Crew, Process

from workflows.crewai.agents import build_agents
from workflows.crewai.config import ensure_local_endpoints_ready
from workflows.crewai.execution import persist_execution_plan
from workflows.crewai.review_gate import approve_review_gate, persist_review_gate, require_approved_review_gate
from workflows.crewai.repository_tools import apply_serialized_write_requests
from workflows.crewai.tasks import build_tasks


def run_architect_only(feature_request: str | None = None) -> str:
    agents = build_agents()
    task = build_tasks(agents, feature_request)["architecture"]
    crew = Crew(
        agents=[agents["architect"]],
        tasks=[task],
        process=Process.sequential,
        verbose=True,
    )
    return kickoff_and_persist(crew, {"architecture": task}, feature_request)


def run_full_workflow(feature_request: str | None = None) -> str:
    require_approved_review_gate(feature_request)
    agents = build_agents()
    tasks = build_tasks(agents, feature_request)
    proposal_names = ["architecture", "tech_lead", "developer_1", "developer_2"]
    proposal_agent_names = ["architect", "tech_lead", "developer_1", "developer_2"]
    proposal_tasks = {name: tasks[name] for name in proposal_names}
    proposal_crew = Crew(
        agents=[agents[name] for name in proposal_agent_names],
        tasks=list(proposal_tasks.values()),
        process=Process.sequential,
        verbose=True,
    )
    kickoff_and_persist(proposal_crew, proposal_tasks, feature_request)

    print("\nPROPOSED CHANGES ARE READY")
    print(f"Review the files in {CREWAI_ARTIFACT_DIR} before continuing.")
    answer = input("Apply these changes to demo-project? (y/n): ").strip().lower()
    if answer != "y":
        persist_run_status(feature_request, "rejected", proposal_names)
        return "Execution stopped. No application changes were approved."

    implementation_tasks = {"implementation": tasks["implementation"]}
    implementation_crew = Crew(
        agents=[agents["implementer"]],
        tasks=list(implementation_tasks.values()),
        process=Process.sequential,
        verbose=True,
    )
    implementation_result = kickoff_and_persist(implementation_crew, implementation_tasks, feature_request)
    raw_output = getattr(tasks["implementation"].output, "raw", "")
    applied = apply_serialized_write_requests(str(raw_output))
    if applied:
        (CREWAI_ARTIFACT_DIR / "applied_changes.json").write_text(
            json.dumps(applied, indent=2), encoding="utf-8"
        )

    follow_up_names = ["tester", "documentation", "deployment"]
    follow_up_tasks = {name: tasks[name] for name in follow_up_names}
    follow_up_crew = Crew(
        agents=[agents[name] for name in follow_up_names],
        tasks=list(follow_up_tasks.values()),
        process=Process.sequential,
        verbose=True,
    )
    follow_up_result = kickoff_and_persist(follow_up_crew, follow_up_tasks, feature_request)
    return f"{implementation_result}\n{follow_up_result}"


def run_developer_preview(feature_request: str | None = None) -> str:
    require_approved_review_gate(feature_request)
    agents = build_agents()
    all_tasks = build_tasks(agents, feature_request)
    preview_task_names = ["architecture", "tech_lead", "developer_1", "developer_2"]
    preview_tasks = {name: all_tasks[name] for name in preview_task_names}
    crew = Crew(
        agents=[agents[name] for name in ("architect", "tech_lead", "developer_1", "developer_2")],
        tasks=list(preview_tasks.values()),
        process=Process.sequential,
        verbose=True,
    )
    return kickoff_and_persist(crew, preview_tasks, feature_request)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the CrewAI local workflow demonstration.")
    parser.add_argument("--full", action="store_true", help="Run the full multi-agent workflow.")
    parser.add_argument(
        "--preview",
        action="store_true",
        help="Run through both developer tasks, persist proposed changes, and stop before testing.",
    )
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Create the execution plan and review gate artifacts without running the full agent loop.",
    )
    parser.add_argument(
        "--review",
        action="store_true",
        help="Generate the plan + diff review gate and stop before execution.",
    )
    parser.add_argument(
        "--approve",
        action="store_true",
        help="Approve the matching review gate so the full workflow can run.",
    )
    parser.add_argument(
        "--feature-request",
        type=str,
        default=None,
        help="Optional feature request to feed into the planning and delivery tasks.",
    )
    args = parser.parse_args()

    if args.review:
        gate = persist_review_gate(args.feature_request)
        print(json.dumps(gate, indent=2))
        raise SystemExit(0)

    if args.approve:
        gate = approve_review_gate(args.feature_request)
        print(json.dumps(gate, indent=2))
        raise SystemExit(0)

    if args.execute:
        plan = persist_execution_plan(args.feature_request)
        gate = persist_review_gate(args.feature_request)
        print(json.dumps({"execution_plan": plan, "review_gate": gate}, indent=2))
        raise SystemExit(0)

    if args.preview:
        ensure_local_endpoints_ready()
        print(run_developer_preview(args.feature_request))
        raise SystemExit(0)

    ensure_local_endpoints_ready()

    if args.full:
        result = run_full_workflow(args.feature_request)
    else:
        result = run_architect_only(args.feature_request)

    print(result)

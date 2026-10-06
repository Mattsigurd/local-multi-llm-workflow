from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from crewai import Crew, Process

from workflows.crewai.agents import build_agents
from workflows.crewai.config import ensure_local_endpoints_ready
from workflows.crewai.execution import persist_execution_plan
from workflows.crewai.review_gate import approve_review_gate, persist_review_gate, require_approved_review_gate
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
    return str(crew.kickoff())


def run_full_workflow(feature_request: str | None = None) -> str:
    require_approved_review_gate(feature_request)
    agents = build_agents()
    tasks = build_tasks(agents, feature_request)
    crew = Crew(
        agents=[
            agents["architect"],
            agents["tech_lead"],
            agents["developer_1"],
            agents["developer_2"],
            agents["tester"],
            agents["documentation"],
            agents["deployment"],
        ],
        tasks=[
            tasks["architecture"],
            tasks["tech_lead"],
            tasks["developer_1"],
            tasks["developer_2"],
            tasks["tester"],
            tasks["documentation"],
            tasks["deployment"],
        ],
        process=Process.sequential,
        verbose=True,
    )
    return str(crew.kickoff())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the CrewAI local workflow demonstration.")
    parser.add_argument("--full", action="store_true", help="Run the full multi-agent workflow.")
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

    ensure_local_endpoints_ready()

    if args.full:
        result = run_full_workflow(args.feature_request)
    else:
        result = run_architect_only(args.feature_request)

    print(result)

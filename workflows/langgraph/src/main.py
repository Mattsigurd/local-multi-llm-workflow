from langgraph.graph import StateGraph, START, END
from langchain_ollama import ChatOllama
from typing import TypedDict
from pathlib import Path
from dotenv import load_dotenv
import subprocess
import sys
import os
import json
from urllib.parse import urlparse


load_dotenv(Path(__file__).resolve().parents[1] / ".env")


class State(TypedDict):
    task: str
    project_context: str
    architecture: str
    plan: str
    tickets: str
    code_proposal: str
    approved: bool
    test_results: str
    test_passed: bool
    documentation: str
    deployment_validation: str


def local_endpoint(variable: str, default: str) -> str:
    endpoint = os.getenv(variable, default).rstrip("/")
    hostname = urlparse(endpoint).hostname
    if hostname not in {"localhost", "127.0.0.1", "::1"}:
        raise ValueError(f"{variable} must point to a local endpoint, got {endpoint}")
    return endpoint


architect_llm = ChatOllama(
    model=os.getenv("ARCHITECT_MODEL", "llama3.2"),
    base_url=local_endpoint("ARCHITECT_ENDPOINT", "http://localhost:11434")
)

developer_llm = ChatOllama(
    model=os.getenv("DEVELOPER_MODEL", "llama3.2"),
    base_url=local_endpoint("DEVELOPER_ENDPOINT", "http://localhost:11435")
)


REPO_ROOT = Path(__file__).resolve().parents[3]
PROJECT_DIR = REPO_ROOT / "demo-project"
ARTIFACT_DIR = REPO_ROOT / "artifacts" / "langgraph"


def write_artifact(filename: str, content: str) -> None:
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    (ARTIFACT_DIR / filename).write_text(content, encoding="utf-8")


def read_project_context() -> str:
    files = [
        PROJECT_DIR / "app" / "main.py",
        PROJECT_DIR / "tests" / "test_main.py",
    ]

    context = ""

    for file in files:
        if file.exists():
            context += f"\n\n===== {file} =====\n"
            context += file.read_text(encoding="utf-8")

    return context


def architect(state: State):
    response = architect_llm.invoke(
        "You are the architect.\n"
        "You must work with the EXISTING project shown below.\n"
        "Do not invent databases, folders, files, models, or technologies.\n"
        "Do not replace the existing architecture.\n\n"
        "EXISTING PROJECT:\n"
        + state["project_context"]
        + "\n\nTASK:\n"
        + state["task"]
        + "\n\n"
        "Give 3-5 short architecture points."
    )

    architecture = response.content

    print("\nARCHITECT:\n" + architecture)

    write_artifact("architecture.md", "# Architecture\n\n" + architecture)

    write_artifact("ADR-001-architecture.md",
        "# ADR-001: Preserve Existing FastAPI Architecture\n\n"
        "## Status\n\n"
        "Accepted\n\n"
        "## Context\n\n"
        "The demo project is an existing FastAPI application with "
        "Pydantic models and an in-memory Todo data store. The workflow "
        "must extend the existing project without replacing its architecture.\n\n"
        "## Decision\n\n"
        "Keep the existing FastAPI/Pydantic architecture and implement "
        "the requested functionality within the existing application structure.\n\n"
        "## Consequences\n\n"
        "- Existing application structure remains unchanged.\n"
        "- The workflow can review changes against the existing project.\n"
        "- The application continues to use its existing in-memory data store.\n\n"
        "## Architecture Analysis\n\n"
        + architecture,
    )

    try:
        result = subprocess.run(
            [
                sys.executable,
                "-c",
                (
                    "from app.main import app; "
                    "import json; "
                    "print(json.dumps(app.openapi(), indent=2))"
                ),
            ],
            cwd=PROJECT_DIR,
            capture_output=True,
            text=True,
            check=True
        )

        write_artifact("openapi.json", result.stdout)

        print("\nOPENAPI: Generated openapi.json")

    except subprocess.CalledProcessError as error:
        print("\nOPENAPI: Could not generate OpenAPI document.")
        print(error.stderr)

    return {"architecture": architecture}


def developer(state: State):
    response = developer_llm.invoke(
        "You are the developer.\n"
        "Create a short implementation plan for the task.\n"
        "Use ONLY the existing project shown below.\n"
        "Do not invent databases, files, folders, or technologies.\n\n"
        "EXISTING PROJECT:\n"
        + state["project_context"]
        + "\n\n"
        "ARCHITECTURE:\n"
        + state["architecture"]
        + "\n\n"
        "TASK:\n"
        + state["task"]
        + "\n\n"
        "Give 2-4 implementation steps."
    )

    plan = response.content

    print("\nDEVELOPER:\n" + plan)

    write_artifact("implementation_plan.md", "# Implementation Plan\n\n" + plan)

    return {"plan": plan}


def tech_lead(state: State):
    response = architect_llm.invoke(
        "You are the tech lead.\n"
        "Turn this implementation plan into exactly 2 small tickets.\n"
        "Each ticket must have a title, scope, acceptance criteria, "
        "dependencies, and definition of done.\n\n"
        + state["plan"]
    )

    tickets = response.content

    print("\nTECH LEAD:\n" + tickets)

    write_artifact("tickets.md", "# Development Tickets\n\n" + tickets)

    return {"tickets": tickets}


def coding_worker_1(state: State):
    response = developer_llm.invoke(
        "You are Coding Worker 1.\n"
        "Work ONLY on Ticket 1.\n"
        "Use the EXISTING PROJECT shown below.\n"
        "Do not invent databases, models, folders, or technologies.\n"
        "Only propose changes that are necessary for the ticket.\n\n"
        "EXISTING PROJECT:\n"
        + state["project_context"]
        + "\n\n"
        "TICKET:\n"
        + state["tickets"]
        + "\n\n"
        "Return proposed file changes only.\n"
        "Use exactly this format:\n"
        "FILE: relative/path/to/file\n"
        "```python\n"
        "complete file contents\n"
        "```"
    )

    proposal = response.content

    print("\nCODING WORKER 1 - PROPOSED CHANGES:\n" + proposal)

    return {"code_proposal": proposal}


def coding_worker_2(state: State):
    response = developer_llm.invoke(
        "You are Coding Worker 2.\n"
        "Work ONLY on Ticket 2.\n"
        "Use the EXISTING PROJECT shown below.\n"
        "Do not invent databases, models, folders, or technologies.\n"
        "Only propose changes that are necessary for the ticket.\n\n"
        "EXISTING PROJECT:\n"
        + state["project_context"]
        + "\n\n"
        "TICKET:\n"
        + state["tickets"]
        + "\n\n"
        "Return proposed file changes only.\n"
        "Use exactly this format:\n"
        "FILE: relative/path/to/file\n"
        "```python\n"
        "complete file contents\n"
        "```"
    )

    proposal = response.content

    print("\nCODING WORKER 2 - PROPOSED CHANGES:\n" + proposal)

    return {
        "code_proposal": state["code_proposal"]
        + "\n\n"
        + proposal
    }


def human_approval(state: State):
    print("\n================================")
    print("PROPOSED CODE CHANGES")
    print("================================")
    print(state["code_proposal"])

    print("\n================================")
    print("HUMAN APPROVAL")
    print("================================")

    answer = input(
        "\nApply these changes to demo-project? (y/n): "
    ).strip().lower()

    if answer == "y":
        print("\nChanges approved.")
        return {"approved": True}

    print("\nChanges rejected. No code changes will be applied.")
    return {"approved": False}


def apply_changes(state: State):
    if not state["approved"]:
        return {}

    proposal = state["code_proposal"]

    sections = proposal.split("FILE:")

    for section in sections[1:]:
        lines = section.strip().splitlines()

        file_path = lines[0].strip()

        code_lines = []
        inside_code = False

        for line in lines[1:]:
            if line.startswith("```"):
                inside_code = not inside_code
                continue

            if inside_code:
                code_lines.append(line)

        if not code_lines:
            continue

        target = PROJECT_DIR / file_path

        target = target.resolve()
        project_root = PROJECT_DIR.resolve()

        try:
            target.relative_to(project_root)
        except ValueError:
            print(f"Skipped unsafe path: {file_path}")
            continue

        target.parent.mkdir(parents=True, exist_ok=True)

        target.write_text(
            "\n".join(code_lines) + "\n",
            encoding="utf-8"
        )

        print(f"Applied: {file_path}")

    return {}


def test_agent(state: State):
    print("\nTEST AGENT: Running pytest...")

    pytest_result = subprocess.run(
        [sys.executable, "-m", "pytest", "tests"],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True
    )

    print("\nTEST AGENT: Running static Python check...")

    compile_result = subprocess.run(
        [
            sys.executable,
            "-m",
            "compileall",
            "-q",
            "app",
            "tests"
        ],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True
    )

    test_results = (
        "# Test & Quality Report\n\n"
        "## Test Execution\n\n"
        f"Return code: {pytest_result.returncode}\n\n"
        "### Pytest Output\n\n"
        "```text\n"
        + pytest_result.stdout
        + "\n```\n\n"
        "### Pytest Errors\n\n"
        "```text\n"
        + pytest_result.stderr
        + "\n```\n\n"
        "## Static Check\n\n"
        "Python bytecode compilation was run against the application and tests.\n\n"
        f"Return code: {compile_result.returncode}\n\n"
        "### Output\n\n"
        "```text\n"
        + compile_result.stdout
        + "\n"
        + compile_result.stderr
        + "\n```\n\n"
        "## Known Limitations and Risks\n\n"
        "- The Todo data is stored in memory and is lost when the application restarts.\n"
        "- AI-generated code may require human review before being applied.\n"
        "- The local LLM endpoints are intended to remain local and should not be exposed publicly without authentication and appropriate security controls.\n"
    )

    print("\nTEST RESULTS:\n" + test_results)

    write_artifact("test-results.md", test_results)

    return {
        "test_results": test_results,
        "test_passed": pytest_result.returncode == 0 and compile_result.returncode == 0,
    }


def route_after_tests(state: State) -> str:
    return "passed" if state["test_passed"] else "failed"


def documentation_agent(state: State):
    response = developer_llm.invoke(
        "You are the documentation agent.\n"
        "Create short documentation for the existing project.\n"
        "Include setup/run instructions, API usage, and basic operational notes.\n"
        "Do not invent databases, technologies, or services.\n\n"
        "EXISTING PROJECT:\n"
        + state["project_context"]
        + "\n\n"
        "TASK:\n"
        + state["task"]
        + "\n\n"
        "ARCHITECTURE:\n"
        + state["architecture"]
        + "\n\n"
        "TEST REPORT:\n"
        + state["test_results"]
    )

    documentation = response.content

    print("\nDOCUMENTATION AGENT:\n" + documentation)

    write_artifact("README.generated.md", "# Todo API\n\n" + documentation)

    return {"documentation": documentation}


def deployment_validation_agent(state: State):
    response = architect_llm.invoke(
        "You are the deployment validation agent.\n"
        "Create a short deployment validation checklist for the EXISTING project.\n"
        "Only include things that can actually be checked for this project.\n"
        "Include application startup, tests, configuration, local LLM endpoints, "
        "and basic security checks.\n"
        "Do not invent infrastructure or services.\n\n"
        "EXISTING PROJECT:\n"
        + state["project_context"]
        + "\n\n"
        "TEST RESULTS:\n"
        + state["test_results"]
        + "\n\n"
        "DOCUMENTATION:\n"
        + state["documentation"]
    )

    deployment_validation = response.content

    print(
        "\nDEPLOYMENT VALIDATION AGENT:\n"
        + deployment_validation
    )

    write_artifact(
        "deployment-checklist.md",
        "# Deployment Validation Checklist\n\n" + deployment_validation,
    )

    return {"deployment_validation": deployment_validation}


graph = StateGraph(State)

graph.add_node("architect", architect)
graph.add_node("developer", developer)
graph.add_node("tech_lead", tech_lead)
graph.add_node("coding_worker_1", coding_worker_1)
graph.add_node("coding_worker_2", coding_worker_2)
graph.add_node("human_approval", human_approval)
graph.add_node("apply_changes", apply_changes)
graph.add_node("test_agent", test_agent)
graph.add_node("documentation_agent", documentation_agent)
graph.add_node(
    "deployment_validation_agent",
    deployment_validation_agent
)

graph.add_edge(START, "architect")
graph.add_edge("architect", "developer")
graph.add_edge("developer", "tech_lead")
graph.add_edge("tech_lead", "coding_worker_1")
graph.add_edge("coding_worker_1", "coding_worker_2")
graph.add_edge("coding_worker_2", "human_approval")
graph.add_edge("human_approval", "apply_changes")
graph.add_edge("apply_changes", "test_agent")
graph.add_conditional_edges(
    "test_agent",
    route_after_tests,
    {"passed": "documentation_agent", "failed": END},
)
graph.add_edge(
    "documentation_agent",
    "deployment_validation_agent"
)
graph.add_edge("deployment_validation_agent", END)

app = graph.compile()


def run_workflow(task: str = "Add a PUT /todos/{todo_id} endpoint that updates an existing Todo."):
    return app.invoke({
        "task": task,
        "project_context": read_project_context(),
        "architecture": "",
        "plan": "",
        "tickets": "",
        "code_proposal": "",
        "approved": False,
        "test_results": "",
        "test_passed": False,
        "documentation": "",
        "deployment_validation": "",
    })


if __name__ == "__main__":
    run_workflow()
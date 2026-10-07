from __future__ import annotations

from crewai import Agent

from .config import LLM_TIMEOUT_SECONDS, build_llm_for_role
from .repository_tools import repository_editing_tools, repository_read_tools, testing_tools


def build_agents() -> dict[str, Agent]:
    return {
        "architect": Agent(
            role="Architect",
            goal="Analyze the feature request and produce a clear architecture plan for the repository.",
            backstory="You reason about the existing Python/FastAPI system and do not invent unrelated technologies.",
            verbose=True,
            llm=build_llm_for_role("architect"),
            allow_delegation=False,
            max_iter=1,
            max_execution_time=LLM_TIMEOUT_SECONDS,
            tools=repository_read_tools(),
        ),
        "tech_lead": Agent(
            role="Tech Lead",
            goal="Convert the architecture plan into executable implementation tasks with acceptance criteria.",
            backstory="You translate the existing Python/FastAPI design into scoped work packages.",
            verbose=True,
            llm=build_llm_for_role("tech_lead"),
            allow_delegation=False,
            max_iter=1,
            max_execution_time=LLM_TIMEOUT_SECONDS,
            tools=repository_read_tools(),
        ),
        "developer_1": Agent(
            role="Developer 1",
            goal="Propose the data-model changes required by the approved feature request.",
            backstory="You inspect the existing project and return a reviewable proposal without modifying files.",
            verbose=True,
            llm=build_llm_for_role("developer_1"),
            allow_delegation=False,
            max_iter=1,
            max_execution_time=LLM_TIMEOUT_SECONDS,
            tools=repository_read_tools(),
        ),
        "developer_2": Agent(
            role="Developer 2",
            goal="Propose the API and integration changes required by the approved feature request.",
            backstory="You inspect the existing project and return a reviewable proposal without modifying files.",
            verbose=True,
            llm=build_llm_for_role("developer_2"),
            allow_delegation=False,
            max_iter=1,
            max_execution_time=LLM_TIMEOUT_SECONDS,
            tools=repository_read_tools(),
        ),
        "implementer": Agent(
            role="Implementation Engineer",
            goal="Apply the approved implementation to the existing FastAPI repository and verify the result.",
            backstory="You implement only an approved change using the controlled repository tools.",
            verbose=True,
            llm=build_llm_for_role("developer_1"),
            allow_delegation=False,
            max_iter=4,
            max_execution_time=LLM_TIMEOUT_SECONDS,
            tools=repository_editing_tools(),
        ),
        "tester": Agent(
            role="Tester",
            goal="Create or improve tests and validate the feature with real commands.",
            backstory="You inspect the code, run the test tool, and report actual results.",
            verbose=True,
            llm=build_llm_for_role("tester"),
            allow_delegation=False,
            max_iter=1,
            max_execution_time=LLM_TIMEOUT_SECONDS,
            tools=testing_tools(),
        ),
        "documentation": Agent(
            role="Documentation Lead",
            goal="Update technical documentation and operational notes after implementation.",
            backstory="You update only documentation relevant to the existing Python/FastAPI project.",
            verbose=True,
            llm=build_llm_for_role("documentation"),
            allow_delegation=False,
            max_iter=1,
            max_execution_time=LLM_TIMEOUT_SECONDS,
            tools=repository_editing_tools(),
        ),
        "deployment": Agent(
            role="Deployment Validator",
            goal="Check repository deployability and release readiness after implementation.",
            backstory="You run available checks and report concrete operational risks.",
            verbose=True,
            llm=build_llm_for_role("deployment"),
            allow_delegation=False,
            max_iter=1,
            max_execution_time=LLM_TIMEOUT_SECONDS,
            tools=testing_tools(),
        ),
    }

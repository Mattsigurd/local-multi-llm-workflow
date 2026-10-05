from __future__ import annotations

from crewai import Agent

from .config import build_llm_for_role


def build_agents() -> dict[str, Agent]:
    return {
        "architect": Agent(
            role="Architect",
            goal="Analyze the feature request and produce a clear architecture plan for the repository.",
            backstory=(
                "You are the architecture lead for a local multi-LLM coding workflow. "
                "You reason about system boundaries, responsibilities, and integration points."
            ),
            verbose=True,
            llm=build_llm_for_role("architect"),
            allow_delegation=False,
        ),
        "tech_lead": Agent(
            role="Tech Lead",
            goal="Convert the architecture plan into executable implementation tasks with acceptance criteria.",
            backstory=(
                "You translate architecture into concrete work packages, sequencing, and definitions of done."
            ),
            verbose=True,
            llm=build_llm_for_role("tech_lead"),
            allow_delegation=False,
        ),
        "developer_1": Agent(
            role="Developer 1",
            goal="Implement the data model and persistence-related changes for the requested feature.",
            backstory="You focus on the schema, object model, and repository layer of the feature.",
            verbose=True,
            llm=build_llm_for_role("developer_1"),
            allow_delegation=False,
        ),
        "developer_2": Agent(
            role="Developer 2",
            goal="Implement the API and integration changes required by the feature request.",
            backstory="You focus on endpoints, validation, and related service integration work.",
            verbose=True,
            llm=build_llm_for_role("developer_2"),
            allow_delegation=False,
        ),
        "tester": Agent(
            role="Tester",
            goal="Create or improve tests and validate the feature with real commands.",
            backstory="You inspect the code, generate missing tests, and report the actual testing result.",
            verbose=True,
            llm=build_llm_for_role("tester"),
            allow_delegation=False,
        ),
        "documentation": Agent(
            role="Documentation Lead",
            goal="Update technical documentation and operational notes so the feature remains understandable.",
            backstory="You maintain accurate README, API, and design documentation for the repository.",
            verbose=True,
            llm=build_llm_for_role("documentation"),
            allow_delegation=False,
        ),
        "deployment": Agent(
            role="Deployment Validator",
            goal="Check repository deployability, Docker configuration, and release readiness.",
            backstory="You ensure the project can be built and deployed with a reasonable validation checklist.",
            verbose=True,
            llm=build_llm_for_role("deployment"),
            allow_delegation=False,
        ),
    }

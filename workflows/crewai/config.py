from __future__ import annotations

import json
import os
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.parse import urlparse

from dotenv import load_dotenv


load_dotenv(Path(__file__).resolve().parent / ".env")


def _endpoint_url(variable: str, default: str) -> str:
    return os.getenv(variable, default).rstrip("/")


LLM_TIMEOUT_SECONDS = int(os.getenv("LLM_TIMEOUT_SECONDS", "300"))

MODEL_ENDPOINTS: dict[str, dict[str, str]] = {
    "planning": {
        "base_url": _endpoint_url("PLANNING_LLM_BASE_URL", "http://localhost:11434"),
        "model": os.getenv("PLANNING_LLM_MODEL", "llama3.2:latest"),
    },
    "coding": {
        "base_url": _endpoint_url("CODING_LLM_BASE_URL", "http://localhost:11435"),
        "model": os.getenv("CODING_LLM_MODEL", "llama3.2:latest"),
    },
}

ROLE_TO_ENDPOINT: dict[str, str] = {
    "architect": "planning",
    "tech_lead": "planning",
    "developer_1": "coding",
    "developer_2": "coding",
    "tester": "coding",
    "documentation": "planning",
    "deployment": "planning",
}


def get_endpoint_for_role(role_name: str) -> dict[str, str]:
    endpoint_name = ROLE_TO_ENDPOINT.get(role_name, "planning")
    return MODEL_ENDPOINTS[endpoint_name]


def is_endpoint_available(base_url: str) -> bool:
    hostname = urlparse(base_url).hostname
    if hostname not in {"localhost", "127.0.0.1", "::1"}:
        return False
    request = Request(f"{base_url.rstrip('/')}/api/tags", headers={"User-Agent": "crewai-workflow"})
    try:
        with urlopen(request, timeout=5) as response:
            payload = json.loads(response.read().decode("utf-8"))
            return bool(payload.get("models"))
    except Exception:
        return False


def ensure_local_endpoints_ready() -> None:
    missing = []
    for name, config in MODEL_ENDPOINTS.items():
        if not is_endpoint_available(config["base_url"]):
            missing.append(f"{name}: {config['base_url']}")

    if missing:
        joined = ", ".join(missing)
        raise RuntimeError(
            "One or more local Ollama-compatible endpoints are unavailable. "
            f"Start them before running the workflow: {joined}"
        )


def build_llm_for_role(role_name: str):
    from crewai import LLM

    endpoint = get_endpoint_for_role(role_name)
    return LLM(
        model=endpoint["model"],
        provider="ollama",
        base_url=endpoint["base_url"],
        api_key="ollama",
        temperature=0.2,
        timeout=LLM_TIMEOUT_SECONDS,
    )

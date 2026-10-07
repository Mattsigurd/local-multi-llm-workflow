from __future__ import annotations

import json
import subprocess
from pathlib import Path

from crewai.tools import BaseTool
from pydantic import BaseModel, Field

ROOT = Path(__file__).resolve().parents[2]
ALLOWED_ROOTS = (ROOT / "demo-project", ROOT / "artifacts" / "crewai")
DEMO_ROOT_NAMES = {"app", "tests", "README.md", "requirements.txt"}


class FilePathInput(BaseModel):
    path: str = Field(description="Repository-relative path to a project file")


class FileWriteInput(FilePathInput):
    content: str = Field(description="Complete replacement contents for the file")


def _safe_path(relative_path: str) -> Path:
    normalized = relative_path.lstrip("/")
    first_part = normalized.split("/", 1)[0]
    if first_part in DEMO_ROOT_NAMES and not normalized.startswith("demo-project/"):
        normalized = f"demo-project/{normalized}"

    target = (ROOT / normalized).resolve()
    if not any(target == allowed or allowed in target.parents for allowed in ALLOWED_ROOTS):
        raise ValueError("Path is outside the approved project and artifact directories")
    return target


class ReadRepositoryFileTool(BaseTool):
    name: str = "read_repository_file"
    description: str = (
        "Read a UTF-8 text file from demo-project or artifacts/crewai. "
        "Use this before proposing or applying a change."
    )
    args_schema: type[BaseModel] = FilePathInput

    def _run(self, path: str) -> str:
        target = _safe_path(path)
        if not target.is_file():
            raise FileNotFoundError(f"File does not exist: {path}")
        return target.read_text(encoding="utf-8")


class WriteRepositoryFileTool(BaseTool):
    name: str = "write_repository_file"
    description: str = (
        "Write complete UTF-8 file contents to demo-project or artifacts/crewai. "
        "This applies a real repository change; only use it after reviewing the requested change."
    )
    args_schema: type[BaseModel] = FileWriteInput

    def _run(self, path: str, content: str) -> str:
        target = _safe_path(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        return f"Applied file change: {target.relative_to(ROOT)}"


class RunDemoTestsTool(BaseTool):
    name: str = "run_demo_tests"
    description: str = "Run the demo project's Pytest suite and return its actual output."

    def _run(self) -> str:
        result = subprocess.run(
            [".venv/bin/python", "-m", "pytest", "demo-project/tests", "-q"],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
        )
        output = (result.stdout + "\n" + result.stderr).strip()
        return f"exit_code={result.returncode}\n{output}"


def repository_editing_tools() -> list[BaseTool]:
    return [ReadRepositoryFileTool(), WriteRepositoryFileTool()]

def repository_read_tools() -> list[BaseTool]:
    return [ReadRepositoryFileTool()]


def testing_tools() -> list[BaseTool]:
    return [ReadRepositoryFileTool(), RunDemoTestsTool()]


def apply_serialized_write_requests(text: str) -> list[str]:
    decoder = json.JSONDecoder()
    applied = []
    position = 0
    while position < len(text):
        start = text.find("{", position)
        if start == -1:
            break
        try:
            payload, end = decoder.raw_decode(text[start:])
        except json.JSONDecodeError:
            position = start + 1
            continue
        position = start + end
        if payload.get("name") != "write_repository_file":
            continue
        parameters = payload.get("parameters", {})
        path = parameters.get("path")
        content = parameters.get("content")
        if isinstance(path, str) and isinstance(content, str):
            applied.append(WriteRepositoryFileTool()._run(path, content))
    return applied

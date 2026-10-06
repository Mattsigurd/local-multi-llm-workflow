import sys
from pathlib import Path

from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.main import app

client = TestClient(app)


def test_health_endpoint() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_todo_with_priority_and_due_date() -> None:
    response = client.post(
        "/todos",
        json={
            "title": "Write assignment summary",
            "description": "Finish the CrewAI workflow notes.",
            "priority": "high",
            "due_date": "2026-10-15",
        },
    )
    assert response.status_code == 201
    body = response.json()
    assert body["title"] == "Write assignment summary"
    assert body["priority"] == "high"
    assert body["due_date"] == "2026-10-15"
    assert body["completed"] is False


def test_get_todo_by_id() -> None:
    response = client.get("/todos/1")
    assert response.status_code == 200
    body = response.json()
    assert body["id"] == 1
    assert body["priority"] in {"low", "medium", "high"}

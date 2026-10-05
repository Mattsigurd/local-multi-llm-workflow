# Demo Project: Todo API

This demo project is intentionally small so the assignment can focus on the comparison between the different multi-agent workflow implementations.

## Features

- FastAPI application for managing todo items
- SQLite-backed persistence is optional for later extension
- Tests confirm that `priority` and `due_date` support work end-to-end

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Then open `http://localhost:8000/docs`.

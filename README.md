Assignment: Local Multi-LLM Coding Workflow Evaluation

## Run a workflow

Start two local Ollama-compatible endpoints first: planning on `localhost:11434` and coding on `localhost:11435`.

Run the approval-gated CrewAI workflow:

```bash
./crewai
```

Run the LangGraph workflow:

```bash
./langgraph
```

Both commands use `.venv/bin/python` and stop with a clear error if either local model endpoint is unavailable. CrewAI allows up to five minutes per agent by default; override it with `LLM_TIMEOUT_SECONDS=600 ./crewai` when local inference is slower.

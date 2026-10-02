# Import tools for building the workflow and defining its state.
from langgraph.graph import StateGraph, START, END
from langchain_ollama import ChatOllama
from typing import TypedDict


# Define the information shared between workflow steps.
class State(TypedDict):
    task: str
    architecture: str
    implementation_plan: str


# Connect to the local Ollama language model.
llm = ChatOllama(
    model="llama3.2",
    base_url="http://localhost:11434"
)


# Ask the model to design a simple architecture.
def architect(state: State):
    response = llm.invoke(
        "You are a software architect. "
        "Explain a simple architecture for this task: "
        + state["task"]
    )

    print("\nARCHITECT:")
    print(response.content)

    return {"architecture": response.content}


# Ask the model to create an implementation plan
# based on the architecture created by the architect.
def developer(state: State):
    response = llm.invoke(
        "You are a software developer. "
        "Based on the following architecture, "
        "create a simple implementation plan:\n\n"
        + state["architecture"]
    )

    print("\nDEVELOPER:")
    print(response.content)

    return {"implementation_plan": response.content}


# Create the workflow using the shared state.
graph = StateGraph(State)

# Add the architect and developer steps.
graph.add_node("architect", architect)
graph.add_node("developer", developer)

# Run the steps in order and then finish.
graph.add_edge(START, "architect")
graph.add_edge("architect", "developer")
graph.add_edge("developer", END)

# Compile the workflow for execution.
app = graph.compile()

# Start the workflow with a task description.
app.invoke({
    "task": "Build a simple task management application",
    "architecture": "",
    "implementation_plan": ""
})
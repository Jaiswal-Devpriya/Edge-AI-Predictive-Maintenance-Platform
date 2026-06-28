from langgraph.graph import StateGraph, END
from typing import TypedDict

from services.incident_agent.knowledge_base import KnowledgeBase
from services.incident_agent.llm_client import AzureOpenAIClient


class IncidentState(TypedDict):
    anomaly: dict
    context: list
    report: str


kb = KnowledgeBase()
llm = AzureOpenAIClient()


def retrieve_context(state: IncidentState):
    anomaly = state["anomaly"]

    query = (
        f"temperature {anomaly['temperature']}, "
        f"pressure {anomaly['pressure']}, "
        f"current {anomaly['current']}, "
        f"severity {anomaly['severity']}"
    )

    context = kb.search(query)

    return {"context": context}


def generate_report(state: IncidentState):
    anomaly = state["anomaly"]
    context = "\n\n".join(state["context"])

    prompt = f"""
You are an industrial predictive maintenance engineer.

Telemetry:
{anomaly}

Relevant historical failures and maintenance runbooks:
{context}

Write a concise incident report with:

1. Summary
2. Likely Root Cause
3. Recommended Actions
4. Priority
"""

    report = llm.generate_incident_report(prompt)

    return {"report": report}


workflow = StateGraph(IncidentState)

workflow.add_node("retrieve_context", retrieve_context)
workflow.add_node("generate_report", generate_report)

workflow.set_entry_point("retrieve_context")

workflow.add_edge("retrieve_context", "generate_report")
workflow.add_edge("generate_report", END)

incident_agent = workflow.compile()
from langgraph.graph import END, START, StateGraph

from app.graph.nodes import (
    extract_signals_node,
    generate_analysis_node,
    get_deployments_node,
    search_incidents_node,
    search_runbooks_node,
)
from app.graph.state import IncidentGraphState


builder = StateGraph(IncidentGraphState)

builder.add_node("extract_signals", extract_signals_node)
builder.add_node("search_incidents", search_incidents_node)
builder.add_node("search_runbooks", search_runbooks_node)
builder.add_node("get_deployments", get_deployments_node)
builder.add_node("generate_analysis", generate_analysis_node)

builder.add_edge(START, "extract_signals")
builder.add_edge("extract_signals", "search_incidents")
builder.add_edge("search_incidents", "search_runbooks")
builder.add_edge("search_runbooks", "get_deployments")
builder.add_edge("get_deployments", "generate_analysis")
builder.add_edge("generate_analysis", END)

incident_workflow = builder.compile()
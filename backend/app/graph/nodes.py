from app.graph.state import IncidentGraphState
from app.services.deployment_service import get_recent_deployments
from app.services.incident_search import search_historical_incidents
from app.services.llm_service import (
    extract_incident_signals,
    generate_incident_analysis,
)
from app.services.runbook_search import search_runbooks


async def extract_signals_node(
    state: IncidentGraphState,
) -> IncidentGraphState:
    signals = await extract_incident_signals(
        service_name=state["service_name"],
        description=state["description"],
        logs=state["logs"],
    )

    return {
        "signals": signals,
        "current_step": "signals_extracted",
    }


def search_incidents_node(
    state: IncidentGraphState,
) -> IncidentGraphState:
    signals = state["signals"]

    incidents = search_historical_incidents(
        service_name=state["service_name"],
        symptoms=[
            *signals.symptoms,
            *signals.error_messages,
        ],
    )

    return {
        "historical_incidents": incidents,
        "current_step": "historical_incidents_searched",
    }


def search_runbooks_node(
    state: IncidentGraphState,
) -> IncidentGraphState:
    signals = state["signals"]

    runbooks = search_runbooks(
        service_name=state["service_name"],
        symptoms=[
            *signals.symptoms,
            *signals.error_messages,
        ],
    )

    return {
        "runbooks": runbooks,
        "current_step": "runbooks_searched",
    }


def get_deployments_node(
    state: IncidentGraphState,
) -> IncidentGraphState:
    deployments = get_recent_deployments(
        service_name=state["service_name"],
    )

    return {
        "deployments": deployments,
        "current_step": "deployments_loaded",
    }


async def generate_analysis_node(
    state: IncidentGraphState,
) -> IncidentGraphState:
    analysis = await generate_incident_analysis(
        service_name=state["service_name"],
        signals=state["signals"],
        historical_incidents=state.get(
            "historical_incidents",
            [],
        ),
        runbooks=state.get("runbooks", []),
        deployments=state.get("deployments", []),
    )

    return {
        "analysis": analysis,
        "current_step": "analysis_completed",
    }
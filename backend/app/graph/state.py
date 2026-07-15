from typing import Any, TypedDict

from app.models.analysis import ExtractedSignals, IncidentAnalysis


class IncidentGraphState(TypedDict, total=False):
    incident_id: str
    service_name: str
    description: str
    logs: str

    signals: ExtractedSignals
    historical_incidents: list[dict[str, Any]]
    runbooks: list[dict[str, Any]]
    deployments: list[dict[str, Any]]
    analysis: IncidentAnalysis

    current_step: str
    error: str | None
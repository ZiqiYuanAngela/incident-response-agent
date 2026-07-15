from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel


class StartAnalysisResponse(BaseModel):
    run_id: str
    incident_id: str
    status: Literal["completed", "failed"]
    current_step: str
    signals: dict[str, Any] | None = None
    historical_incidents: list[dict[str, Any]]
    runbooks: list[dict[str, Any]]
    deployments: list[dict[str, Any]]
    analysis: dict[str, Any] | None = None
    error: str | None = None


class AnalysisRunResponse(BaseModel):
    id: str
    incident_id: str
    status: str
    current_step: str

    signals: dict[str, Any] | None
    historical_incidents: list[dict[str, Any]]
    runbooks: list[dict[str, Any]]
    deployments: list[dict[str, Any]]
    analysis: dict[str, Any] | None

    error: str | None
    started_at: datetime
    completed_at: datetime | None
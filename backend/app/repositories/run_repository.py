import json
from datetime import UTC, datetime
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.tables import AnalysisRunTable
from app.graph.state import IncidentGraphState


class AnalysisRunNotFoundError(ValueError):
    pass


def create_analysis_run(
    db: Session,
    incident_id: str,
) -> AnalysisRunTable:
    run = AnalysisRunTable(
        incident_id=incident_id,
        status="started",
        current_step="started",
    )

    db.add(run)
    db.commit()
    db.refresh(run)

    return run


def get_analysis_run(
    db: Session,
    run_id: str,
) -> AnalysisRunTable:
    statement = select(AnalysisRunTable).where(
        AnalysisRunTable.id == run_id
    )

    run = db.scalar(statement)

    if run is None:
        raise AnalysisRunNotFoundError(
            f"Analysis run not found: {run_id}"
        )

    return run


def complete_analysis_run(
    db: Session,
    run_id: str,
    state: IncidentGraphState,
) -> AnalysisRunTable:
    run = get_analysis_run(db, run_id)

    run.status = "completed"
    run.current_step = state.get(
        "current_step",
        "analysis_completed",
    )

    run.signals_json = serialize_value(state.get("signals"))
    run.historical_incidents_json = serialize_value(
        state.get("historical_incidents", [])
    )
    run.runbooks_json = serialize_value(
        state.get("runbooks", [])
    )
    run.deployments_json = serialize_value(
        state.get("deployments", [])
    )
    run.analysis_json = serialize_value(
        state.get("analysis")
    )

    run.completed_at = datetime.now(UTC)
    run.error = None

    db.commit()
    db.refresh(run)

    return run


def fail_analysis_run(
    db: Session,
    run_id: str,
    error: str,
    current_step: str = "failed",
) -> AnalysisRunTable:
    run = get_analysis_run(db, run_id)

    run.status = "failed"
    run.current_step = current_step
    run.error = error
    run.completed_at = datetime.now(UTC)

    db.commit()
    db.refresh(run)

    return run


def serialize_value(value: Any) -> str | None:
    if value is None:
        return None

    if hasattr(value, "model_dump"):
        value = value.model_dump()

    return json.dumps(
        value,
        default=str,
    )


def deserialize_value(value: str | None) -> Any:
    if value is None:
        return None

    return json.loads(value)
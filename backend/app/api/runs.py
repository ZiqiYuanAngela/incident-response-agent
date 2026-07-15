from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.engine import get_db
from app.models.run import AnalysisRunResponse
from app.repositories.run_repository import (
    AnalysisRunNotFoundError,
    deserialize_value,
    get_analysis_run,
)


router = APIRouter(
    prefix="/api/runs",
    tags=["analysis runs"],
)


@router.get(
    "/{run_id}",
    response_model=AnalysisRunResponse,
)
def get_run_route(
    run_id: str,
    db: Session = Depends(get_db),
) -> AnalysisRunResponse:
    try:
        run = get_analysis_run(db, run_id)
    except AnalysisRunNotFoundError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc

    return AnalysisRunResponse(
        id=run.id,
        incident_id=run.incident_id,
        status=run.status,
        current_step=run.current_step,
        signals=deserialize_value(run.signals_json),
        historical_incidents=(
            deserialize_value(
                run.historical_incidents_json
            )
            or []
        ),
        runbooks=(
            deserialize_value(run.runbooks_json)
            or []
        ),
        deployments=(
            deserialize_value(run.deployments_json)
            or []
        ),
        analysis=deserialize_value(run.analysis_json),
        error=run.error,
        started_at=run.started_at,
        completed_at=run.completed_at,
    )
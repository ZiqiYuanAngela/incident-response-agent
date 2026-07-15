from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.engine import get_db
from app.graph.workflow import incident_workflow
from app.models.incident import (
    CreateIncidentRequest,
    IncidentResponse,
)
from app.models.run import StartAnalysisResponse
from app.repositories.incident_repository import (
    IncidentNotFoundError,
    create_incident,
    get_incident,
    update_incident_status,
)
from app.repositories.run_repository import (
    complete_analysis_run,
    create_analysis_run,
    fail_analysis_run,
)


router = APIRouter(
    prefix="/api/incidents",
    tags=["incidents"],
)


@router.post(
    "",
    response_model=IncidentResponse,
    status_code=201,
)
def create_incident_route(
    request: CreateIncidentRequest,
    db: Session = Depends(get_db),
) -> IncidentResponse:
    incident = create_incident(db, request)
    return IncidentResponse.model_validate(incident)


@router.get(
    "/{incident_id}",
    response_model=IncidentResponse,
)
def get_incident_route(
    incident_id: str,
    db: Session = Depends(get_db),
) -> IncidentResponse:
    try:
        incident = get_incident(db, incident_id)
    except IncidentNotFoundError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc

    return IncidentResponse.model_validate(incident)


@router.post(
    "/{incident_id}/analyze",
    response_model=StartAnalysisResponse,
)
async def analyze_incident_route(
    incident_id: str,
    db: Session = Depends(get_db),
) -> StartAnalysisResponse:
    try:
        incident = get_incident(db, incident_id)
    except IncidentNotFoundError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc

    update_incident_status(
        db,
        incident_id,
        "analyzing",
    )

    run = create_analysis_run(
        db,
        incident_id,
    )

    initial_state = {
        "incident_id": incident.id,
        "service_name": incident.service_name,
        "description": incident.description,
        "logs": incident.logs,
        "current_step": "started",
        "error": None,
    }

    try:
        final_state = await incident_workflow.ainvoke(
            initial_state
        )

        completed_run = complete_analysis_run(
            db=db,
            run_id=run.id,
            state=final_state,
        )

        update_incident_status(
            db,
            incident_id,
            "completed",
        )

        signals = final_state.get("signals")
        analysis = final_state.get("analysis")

        return StartAnalysisResponse(
            run_id=completed_run.id,
            incident_id=incident_id,
            status="completed",
            current_step=completed_run.current_step,
            signals=(
                signals.model_dump()
                if signals is not None
                else None
            ),
            historical_incidents=final_state.get(
                "historical_incidents",
                [],
            ),
            runbooks=final_state.get(
                "runbooks",
                [],
            ),
            deployments=final_state.get(
                "deployments",
                [],
            ),
            analysis=(
                analysis.model_dump()
                if analysis is not None
                else None
            ),
        )
    except Exception as exc:
        # Log the actual exception for debugging
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Incident analysis failed: {str(exc)}", exc_info=True)
        
        fail_analysis_run(
            db=db,
            run_id=run.id,
            error=str(exc),
        )
        
        update_incident_status(
            db,
            incident_id,
            "failed",
        )
        
        # Return more helpful error details
        raise HTTPException(
            status_code=500,
            detail=f"Incident analysis failed: {str(exc)}",
        ) from exc
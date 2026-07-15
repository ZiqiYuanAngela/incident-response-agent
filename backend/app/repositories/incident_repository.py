from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.tables import IncidentTable
from app.models.incident import CreateIncidentRequest


class IncidentNotFoundError(ValueError):
    pass


def create_incident(
    db: Session,
    request: CreateIncidentRequest,
) -> IncidentTable:
    incident = IncidentTable(
        service_name=request.service_name,
        description=request.description,
        logs=request.logs,
        status="created",
    )

    db.add(incident)
    db.commit()
    db.refresh(incident)

    return incident


def get_incident(
    db: Session,
    incident_id: str,
) -> IncidentTable:
    statement = select(IncidentTable).where(
        IncidentTable.id == incident_id
    )

    incident = db.scalar(statement)

    if incident is None:
        raise IncidentNotFoundError(
            f"Incident not found: {incident_id}"
        )

    return incident


def update_incident_status(
    db: Session,
    incident_id: str,
    status: str,
) -> IncidentTable:
    incident = get_incident(db, incident_id)
    incident.status = status

    db.commit()
    db.refresh(incident)

    return incident
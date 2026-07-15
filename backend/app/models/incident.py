from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

class CreateIncidentRequest(BaseModel):
    service_name: str = Field(..., min_length=2, max_length=100, description="The name of the service affected by the incident")
    description: str = Field(..., min_length=5, max_length=5000, description="A detailed description of the incident")
    logs: str = Field(..., min_length=5, max_length=30_000, description="Relevant logs or error messages associated with the incident")

class IncidentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    service_name: str
    description: str
    logs: str
    status: Literal["created", "analyzing", "completed", "failed"]
    created_at: datetime 
    updated_at: datetime
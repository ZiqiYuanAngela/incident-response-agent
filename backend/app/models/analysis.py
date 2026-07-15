from typing import Literal

from pydantic import BaseModel, Field

class ExtractedSignals(BaseModel):
    error_messages: list[str] = Field(default_factory=list, description="A list of error messages extracted from the logs")
    symptoms: list[str] = Field(default_factory=list, description="A list of symptoms extracted from the logs")
    affected_components: list[str] = Field(default_factory=list, description="A list of affected components extracted from the logs")
    severity: Literal["low", "medium", "high", "critical"] = Field(..., description="The severity level of the incident")
    concise_summary: str

class Evidence(BaseModel):
    source_type: Literal["log", "historical_incident", "runbook", "deployment"]
    source_id: str 
    description: str

class RootCauseAnalysis(BaseModel):
    cause: str
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence level of the root cause analysis, between 0 and 1")
    evidence: list[Evidence] = Field(default_factory=list, description="A list of evidence supporting the root cause analysis")

class IncidentAnalysis(BaseModel):
    severity: Literal["low", "medium", "high", "critical"]
    summary: str
    symptoms: list[str]
    hypotheses: list[RootCauseAnalysis]
    investigation_steps: list[str]
    recommended_next_action: str
    limitations: list[str] = Field(default_factory=list, description="A list of limitations or uncertainties in the analysis")
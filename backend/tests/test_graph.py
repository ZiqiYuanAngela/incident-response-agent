from app.graph.workflow import incident_workflow
from app.models.analysis import (
    Evidence,
    ExtractedSignals,
    IncidentAnalysis,
    RootCauseHypothesis,
)


async def fake_extract_incident_signals(
    service_name: str,
    description: str,
    logs: str,
) -> ExtractedSignals:
    return ExtractedSignals(
        error_messages=[
            "Database connection timed out",
        ],
        symptoms=[
            "database connection timeout",
            "connection pool utilization at 100%",
        ],
        affected_components=["database"],
        severity="high",
        concise_summary=(
            "Payment requests cannot acquire database "
            "connections."
        ),
    )


async def fake_generate_incident_analysis(
    service_name: str,
    signals: ExtractedSignals,
    historical_incidents: list[dict],
    runbooks: list[dict],
    deployments: list[dict],
) -> IncidentAnalysis:
    return IncidentAnalysis(
        severity="high",
        summary="The database connection pool may be exhausted.",
        symptoms=signals.symptoms,
        hypotheses=[
            RootCauseHypothesis(
                cause="Database connection pool exhaustion",
                confidence=0.9,
                evidence=[
                    Evidence(
                        source_type="log",
                        source_id="submitted-logs",
                        description=(
                            "Connection pool utilization "
                            "reached 100%."
                        ),
                    ),
                    Evidence(
                        source_type="historical_incident",
                        source_id="INC-001",
                        description=(
                            "A previous incident showed "
                            "similar symptoms."
                        ),
                    ),
                ],
            )
        ],
        investigation_steps=[
            "Inspect active database connections.",
            "Compare connection-pool configuration.",
        ],
        recommended_next_action=(
            "Validate the connection-pool configuration "
            "before considering a rollback."
        ),
        limitations=[],
    )


async def test_incident_workflow(
    monkeypatch,
):
    monkeypatch.setattr(
        "app.graph.nodes.extract_incident_signals",
        fake_extract_incident_signals,
    )

    monkeypatch.setattr(
        "app.graph.nodes.generate_incident_analysis",
        fake_generate_incident_analysis,
    )

    state = {
        "incident_id": "test-incident",
        "service_name": "payment-service",
        "description": (
            "Payments are timing out after deployment."
        ),
        "logs": (
            "ERROR Database connection timed out\n"
            "WARN Connection pool utilization: 100%"
        ),
        "current_step": "started",
        "error": None,
    }

    result = await incident_workflow.ainvoke(state)

    assert result["current_step"] == "analysis_completed"

    assert result["signals"].severity == "high"

    assert any(
        incident["id"] == "INC-001"
        for incident in result["historical_incidents"]
    )

    assert any(
        runbook["id"] == "RB-001"
        for runbook in result["runbooks"]
    )

    assert result["deployments"][0]["id"] == "DEP-101"

    assert (
        result["analysis"]
        .hypotheses[0]
        .cause
        == "Database connection pool exhaustion"
    )
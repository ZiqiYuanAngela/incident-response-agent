from fastapi.testclient import TestClient

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
        error_messages=["Database timeout"],
        symptoms=[
            "database connection timeout",
            "connection pool utilization at 100%",
        ],
        affected_components=["database"],
        severity="high",
        concise_summary=(
            "Database connections are unavailable."
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
        summary="Connection pool exhaustion is likely.",
        symptoms=signals.symptoms,
        hypotheses=[
            RootCauseHypothesis(
                cause="Database connection pool exhaustion",
                confidence=0.88,
                evidence=[
                    Evidence(
                        source_type="log",
                        source_id="submitted-logs",
                        description=(
                            "Pool utilization reached 100%."
                        ),
                    )
                ],
            )
        ],
        investigation_steps=[
            "Inspect active database connections.",
        ],
        recommended_next_action=(
            "Review database pool settings."
        ),
        limitations=[],
    )


def test_create_get_analyze_and_retrieve_run(
    client: TestClient,
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

    create_response = client.post(
        "/api/incidents",
        json={
            "service_name": "payment-service",
            "description": (
                "Payment requests are timing out."
            ),
            "logs": (
                "ERROR Database connection timed out\n"
                "WARN Connection pool utilization: 100%"
            ),
        },
    )

    assert create_response.status_code == 201

    incident = create_response.json()
    incident_id = incident["id"]

    get_response = client.get(
        f"/api/incidents/{incident_id}"
    )

    assert get_response.status_code == 200
    assert (
        get_response.json()["service_name"]
        == "payment-service"
    )

    analyze_response = client.post(
        f"/api/incidents/{incident_id}/analyze"
    )

    assert analyze_response.status_code == 200

    analysis = analyze_response.json()

    assert analysis["status"] == "completed"
    assert analysis["analysis"]["severity"] == "high"
    assert analysis["historical_incidents"]
    assert analysis["runbooks"]
    assert analysis["deployments"]

    run_id = analysis["run_id"]

    run_response = client.get(
        f"/api/runs/{run_id}"
    )

    assert run_response.status_code == 200

    stored_run = run_response.json()

    assert stored_run["status"] == "completed"

    assert (
        stored_run["analysis"]["hypotheses"][0]["cause"]
        == "Database connection pool exhaustion"
    )


def test_get_unknown_incident_returns_404(
    client: TestClient,
):
    response = client.get(
        "/api/incidents/not-a-real-id"
    )

    assert response.status_code == 404
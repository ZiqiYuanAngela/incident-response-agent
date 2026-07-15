from app.services.deployment_service import (
    get_recent_deployments,
)
from app.services.incident_search import (
    search_historical_incidents,
)
from app.services.runbook_search import (
    search_runbooks,
)


def test_payment_database_symptoms_find_incidents():
    results = search_historical_incidents(
        service_name="payment-service",
        symptoms=[
            "database connection timeout",
            "connection pool utilization 100%",
        ],
    )

    ids = [result["id"] for result in results]

    assert "INC-001" in ids


def test_payment_search_does_not_return_order_incident():
    results = search_historical_incidents(
        service_name="payment-service",
        symptoms=["redis timeout"],
    )

    ids = [result["id"] for result in results]

    assert "INC-003" not in ids


def test_database_symptoms_find_database_runbook():
    results = search_runbooks(
        service_name="payment-service",
        symptoms=[
            "database timeout",
            "connection pool",
        ],
    )

    ids = [result["id"] for result in results]

    assert "RB-001" in ids


def test_recent_deployments_are_newest_first():
    deployments = get_recent_deployments(
        service_name="payment-service"
    )

    assert len(deployments) >= 2
    assert deployments[0]["id"] == "DEP-101"
    assert deployments[1]["id"] == "DEP-100"
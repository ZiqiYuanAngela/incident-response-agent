from typing import Any

from app.seed.synthetic_data import DEPLOYMENTS


def get_recent_deployments(
    service_name: str,
    limit: int = 3,
) -> list[dict[str, Any]]:
    matching = [
        deployment
        for deployment in DEPLOYMENTS
        if deployment["service_name"] == service_name
    ]

    matching.sort(
        key=lambda deployment: deployment["deployed_at"],
        reverse=True,
    )

    return matching[:limit]
import re
from typing import Any

from app.seed.synthetic_data import HISTORICAL_INCIDENTS


def tokenize(value: str) -> set[str]:
    return {
        token
        for token in re.findall(r"[a-z0-9]+", value.lower())
        if len(token) > 2
    }


def search_historical_incidents(
    service_name: str,
    symptoms: list[str],
    limit: int = 3,
) -> list[dict[str, Any]]:
    query_tokens = tokenize(" ".join(symptoms))
    ranked: list[tuple[float, dict[str, Any]]] = []

    for incident in HISTORICAL_INCIDENTS:
        if incident["service_name"] != service_name:
            continue

        incident_tokens = tokenize(
            " ".join(
                [
                    incident["title"],
                    *incident["symptoms"],
                    incident["root_cause"],
                ]
            )
        )

        overlap = query_tokens & incident_tokens
        score = len(overlap) / max(len(query_tokens), 1)

        if score > 0:
            ranked.append((score, incident))

    ranked.sort(key=lambda item: item[0], reverse=True)

    return [
        {
            **incident,
            "relevance_score": round(score, 3),
        }
        for score, incident in ranked[:limit]
    ]


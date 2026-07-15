from typing import Any

from app.seed.synthetic_data import RUNBOOKS
from app.services.incident_search import tokenize


def search_runbooks(
    service_name: str,
    symptoms: list[str],
    limit: int = 3,
) -> list[dict[str, Any]]:
    query_tokens = tokenize(" ".join(symptoms))
    ranked: list[tuple[int, dict[str, Any]]] = []

    for runbook in RUNBOOKS:
        if runbook["service_name"] != service_name:
            continue

        runbook_tokens = tokenize(
            " ".join(
                [
                    runbook["title"],
                    *runbook["keywords"],
                    *runbook["steps"],
                ]
            )
        )

        score = len(query_tokens & runbook_tokens)

        if score > 0:
            ranked.append((score, runbook))

    ranked.sort(key=lambda item: item[0], reverse=True)

    return [
        {
            **runbook,
            "relevance_score": score,
        }
        for score, runbook in ranked[:limit]
    ]
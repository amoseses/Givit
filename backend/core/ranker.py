from __future__ import annotations

from backend.utils.scoring import (
    compute_budget_score,
    compute_final_score,
    compute_learned_score,
    compute_match_score,
)


def rank(products: list[dict], tags: list[str], budget: float) -> list[dict]:
    ranked: list[dict] = []

    for product in products:
        metrics = product.get("metrics", {})
        learned_score = compute_learned_score(metrics)
        match_score = compute_match_score(product.get("tags", []), tags)
        budget_score = compute_budget_score(product.get("price", 0.0), budget)
        final_score = compute_final_score(match_score, learned_score, budget_score)

        ranked.append(
            {
                **product,
                "match_score": round(match_score, 6),
                "budget_score": round(budget_score, 6),
                "learned_score": round(learned_score, 6),
                "final_score": round(final_score, 6),
            }
        )

    return sorted(ranked, key=lambda item: (-item["final_score"], item["id"]))

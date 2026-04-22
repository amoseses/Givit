from __future__ import annotations


def compute_learned_score(metrics: dict) -> float:
    positive_feedback = metrics.get("positive_feedback", 0)
    clicks = metrics.get("clicks", 0)
    views = metrics.get("views", 0)
    negative_feedback = metrics.get("negative_feedback", 0)

    raw_score = (positive_feedback * 2 + clicks) / (views + negative_feedback + 1)
    return round(raw_score, 6)


def normalize_learned_score(learned_score: float) -> float:
    return learned_score / (learned_score + 1) if learned_score > 0 else 0.0


def compute_match_score(product_tags: list[str], requested_tags: list[str]) -> float:
    if not requested_tags:
        return 0.5

    if not product_tags:
        return 0.0

    overlap = len(set(product_tags) & set(requested_tags))
    return overlap / len(set(requested_tags))


def compute_budget_score(price: float, budget: float) -> float:
    if budget <= 0:
        return 0.0

    distance = abs(price - budget)
    return max(0.0, 1 - (distance / (budget + 1)))


def compute_final_score(match_score: float, learned_score: float, budget_score: float) -> float:
    normalized_learned = normalize_learned_score(learned_score)
    final_score = 0.5 * match_score + 0.3 * normalized_learned + 0.2 * budget_score
    return round(final_score, 6)


def compute_feedback_ratio(products: list[dict]) -> float:
    positive = sum(product.get("metrics", {}).get("positive_feedback", 0) for product in products)
    negative = sum(product.get("metrics", {}).get("negative_feedback", 0) for product in products)
    total = positive + negative
    if total == 0:
        return 0.0
    return round(positive / total, 6)


def compute_average_top_score(ranked_products: list[dict], top_n: int = 5) -> float:
    if not ranked_products:
        return 0.0

    selected = ranked_products[:top_n]
    average = sum(item.get("final_score", 0.0) for item in selected) / len(selected)
    return round(average, 6)

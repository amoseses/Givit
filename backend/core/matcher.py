def match_products(products: list[dict], tags: list[str], budget: float) -> list[tuple[dict, float]]:
    results: list[tuple[dict, float]] = []

    for product in products:
        score = 0.0

        for tag in tags:
            if tag in product.get("tags", []):
                score += 3

        if product.get("price", 0) <= budget:
            score += 2
        else:
            score -= 2

        if score > 0:
            matched = {**product, "score": score}
            results.append((matched, score))

    return sorted(results, key=lambda item: item[1], reverse=True)

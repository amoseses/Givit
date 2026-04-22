from __future__ import annotations


def match_products(products: list[dict], tags: list[str], budget: float) -> list[dict]:
    if not products:
        return []

    if not tags:
        return [dict(product) for product in products]

    filtered: list[dict] = []
    for product in products:
        product_tags = product.get("tags", [])
        has_overlap = bool(set(product_tags) & set(tags))
        within_reasonable_budget = budget <= 0 or product.get("price", 0) <= budget * 1.5

        if has_overlap and within_reasonable_budget:
            filtered.append(dict(product))

    return filtered or [dict(product) for product in products]

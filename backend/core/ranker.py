def rank(products: list[dict]) -> list[dict]:
    return sorted(
        products,
        key=lambda product: (
            product.get("score", 0) * 2
            + product.get("popularity", 0)
            + product.get("feedback_score", 0)
        ),
        reverse=True,
    )

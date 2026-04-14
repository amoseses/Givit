from backend.db.database import load_products, save_products


def main() -> None:
    products = load_products()
    products.sort(key=lambda product: product.get("popularity", 0) + product.get("feedback_score", 0), reverse=True)

    for index, product in enumerate(products, start=1):
        product["score"] = len(products) - index + 1

    save_products(products)
    print("Updated product scores")


if __name__ == "__main__":
    main()

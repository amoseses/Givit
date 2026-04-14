import json
from pathlib import Path

DATA_DIR = Path("data")
PRODUCTS_PATH = DATA_DIR / "products.json"
FEEDBACK_PATH = DATA_DIR / "feedback.json"


def load_products() -> list[dict]:
    with PRODUCTS_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_products(products: list[dict]) -> None:
    with PRODUCTS_PATH.open("w", encoding="utf-8") as file:
        json.dump(products, file, indent=2)


def append_feedback(record: dict) -> None:
    feedback = []
    if FEEDBACK_PATH.exists():
        with FEEDBACK_PATH.open("r", encoding="utf-8") as file:
            feedback = json.load(file)

    feedback.append(record)

    with FEEDBACK_PATH.open("w", encoding="utf-8") as file:
        json.dump(feedback, file, indent=2)

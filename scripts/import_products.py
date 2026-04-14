import argparse
import json
from pathlib import Path

from backend.db.database import save_products


def main() -> None:
    parser = argparse.ArgumentParser(description="Import products from a JSON file into data/products.json")
    parser.add_argument("input_file", help="Path to source JSON file")
    args = parser.parse_args()

    path = Path(args.input_file)
    with path.open("r", encoding="utf-8") as file:
        products = json.load(file)

    save_products(products)
    print(f"Imported {len(products)} products")


if __name__ == "__main__":
    main()

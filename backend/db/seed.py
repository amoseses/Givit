from backend.db.database import save_products


SEED_PRODUCTS = [
    {
        "id": 1,
        "title": "Ceramic Baking Set",
        "tags": ["baking", "kitchen", "cooking", "giftable"],
        "price": 35,
        "vendor": "Hive Vendor A",
        "popularity": 12,
    },
    {
        "id": 2,
        "title": "Smart Herb Garden",
        "tags": ["kitchen", "tech", "gadgets", "home"],
        "price": 48,
        "vendor": "Hive Vendor B",
        "popularity": 20,
    },
    {
        "id": 3,
        "title": "Aromatherapy Blanket",
        "tags": ["comfort", "home", "self-care", "relaxation"],
        "price": 42,
        "vendor": "Hive Vendor C",
        "popularity": 10,
    },
    {
        "id": 4,
        "title": "Mini Fitness Tracker",
        "tags": ["fitness", "gym", "health", "electronics"],
        "price": 55,
        "vendor": "Hive Vendor D",
        "popularity": 18,
    },
]


if __name__ == "__main__":
    save_products(SEED_PRODUCTS)
    print("Seeded products.json")

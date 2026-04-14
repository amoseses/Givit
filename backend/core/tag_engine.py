TAG_MAP: dict[str, list[str]] = {
    "cooking": ["kitchen", "baking", "food", "chef"],
    "fitness": ["gym", "health", "yoga"],
    "art": ["painting", "creative", "design"],
    "tech": ["gadgets", "electronics"],
    "mom": ["home", "comfort", "self-care"],
    "birthday": ["celebration", "giftable"],
}


def extract_tags(user_input: dict) -> list[str]:
    tags: set[str] = set()

    interest = user_input.get("interest")
    if isinstance(interest, str):
        tags.update(TAG_MAP.get(interest.lower(), []))
        tags.add(interest.lower())

    for value in user_input.get("interests", []):
        if isinstance(value, str):
            tags.update(TAG_MAP.get(value.lower(), []))
            tags.add(value.lower())

    for field in ("relationship", "occasion"):
        value = user_input.get(field)
        if isinstance(value, str):
            tags.update(TAG_MAP.get(value.lower(), []))

    return sorted(tags)

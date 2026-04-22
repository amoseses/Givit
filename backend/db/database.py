from __future__ import annotations

import json
import threading
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path

from backend.core.ranker import rank
from backend.utils.scoring import compute_average_top_score, compute_feedback_ratio, compute_learned_score

DATA_DIR = Path("data")
PRODUCTS_PATH = DATA_DIR / "products.json"
FEEDBACK_PATH = DATA_DIR / "feedback.json"
METRICS_PATH = DATA_DIR / "metrics.json"

_LOCK = threading.RLock()
_STATE: dict[str, list[dict] | dict | bool] = {
    "initialized": False,
    "products": [],
    "feedback": [],
    "metrics": {"history": []},
}

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


def _read_json(path: Path, fallback: list | dict) -> list | dict:
    if not path.exists():
        return deepcopy(fallback)

    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return deepcopy(fallback)


def _atomic_write_json(path: Path, payload: list | dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = path.with_suffix(f"{path.suffix}.tmp")
    temp_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    temp_path.replace(path)


def _ensure_product_shape(product: dict) -> dict:
    metrics = product.get("metrics", {})

    positive_seed = max(product.get("feedback_score", 0), 0)
    negative_seed = abs(min(product.get("feedback_score", 0), 0))

    metrics = {
        "views": int(metrics.get("views", 0)),
        "clicks": int(metrics.get("clicks", 0)),
        "positive_feedback": int(metrics.get("positive_feedback", positive_seed)),
        "negative_feedback": int(metrics.get("negative_feedback", negative_seed)),
    }

    normalized = {
        "id": int(product["id"]),
        "title": product.get("title", ""),
        "tags": list(product.get("tags", [])),
        "price": float(product.get("price", 0)),
        "vendor": product.get("vendor", ""),
        "popularity": int(product.get("popularity", 0)),
        "metrics": metrics,
    }
    normalized["learned_score"] = compute_learned_score(metrics)
    return normalized


def initialize_database() -> None:
    with _LOCK:
        DATA_DIR.mkdir(parents=True, exist_ok=True)

        if not PRODUCTS_PATH.exists():
            _atomic_write_json(PRODUCTS_PATH, SEED_PRODUCTS)
        if not FEEDBACK_PATH.exists():
            _atomic_write_json(FEEDBACK_PATH, [])
        if not METRICS_PATH.exists():
            _atomic_write_json(METRICS_PATH, {"history": []})

        raw_products = _read_json(PRODUCTS_PATH, SEED_PRODUCTS)
        products = [_ensure_product_shape(product) for product in raw_products if "id" in product]

        feedback = _read_json(FEEDBACK_PATH, [])
        metrics = _read_json(METRICS_PATH, {"history": []})
        if not isinstance(metrics, dict) or "history" not in metrics:
            metrics = {"history": []}

        _STATE["products"] = products
        _STATE["feedback"] = feedback if isinstance(feedback, list) else []
        _STATE["metrics"] = metrics
        _STATE["initialized"] = True

        _persist_products_unlocked()


def _ensure_initialized() -> None:
    if not _STATE["initialized"]:
        initialize_database()


def _persist_products_unlocked() -> None:
    products = _STATE["products"]
    assert isinstance(products, list)
    _atomic_write_json(PRODUCTS_PATH, products)


def _persist_feedback_unlocked() -> None:
    feedback = _STATE["feedback"]
    assert isinstance(feedback, list)
    _atomic_write_json(FEEDBACK_PATH, feedback)


def _persist_metrics_unlocked() -> None:
    metrics = _STATE["metrics"]
    assert isinstance(metrics, dict)
    _atomic_write_json(METRICS_PATH, metrics)


def _record_metrics_unlocked(event: str, ranked_products: list[dict] | None = None) -> None:
    products = _STATE["products"]
    metrics = _STATE["metrics"]
    assert isinstance(products, list)
    assert isinstance(metrics, dict)

    if ranked_products is None:
        ranked_products = rank(products, tags=[], budget=0)

    history = metrics.setdefault("history", [])
    if not isinstance(history, list):
        history = []
        metrics["history"] = history

    history.append(
        {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event": event,
            "average_top5_score": compute_average_top_score(ranked_products, top_n=5),
            "feedback_ratio": compute_feedback_ratio(products),
        }
    )


def load_products() -> list[dict]:
    with _LOCK:
        _ensure_initialized()
        products = _STATE["products"]
        assert isinstance(products, list)
        return deepcopy(products)


def save_products(products: list[dict]) -> None:
    with _LOCK:
        _ensure_initialized()
        _STATE["products"] = [_ensure_product_shape(product) for product in products if "id" in product]
        _persist_products_unlocked()


def load_feedback() -> list[dict]:
    with _LOCK:
        _ensure_initialized()
        feedback = _STATE["feedback"]
        assert isinstance(feedback, list)
        return deepcopy(feedback)


def load_metrics() -> dict:
    with _LOCK:
        _ensure_initialized()
        metrics = _STATE["metrics"]
        assert isinstance(metrics, dict)
        return deepcopy(metrics)


def track_recommendation_views(product_ids: list[int], ranked_products: list[dict]) -> None:
    with _LOCK:
        _ensure_initialized()
        products = _STATE["products"]
        assert isinstance(products, list)

        ids = set(product_ids)
        for product in products:
            if product["id"] in ids:
                product["metrics"]["views"] += 1
                product["learned_score"] = compute_learned_score(product["metrics"])

        _record_metrics_unlocked(event="recommend", ranked_products=ranked_products)
        _persist_products_unlocked()
        _persist_metrics_unlocked()


def record_feedback(product_id: int, action: str) -> dict:
    with _LOCK:
        _ensure_initialized()
        products = _STATE["products"]
        feedback = _STATE["feedback"]
        assert isinstance(products, list)
        assert isinstance(feedback, list)

        target = next((product for product in products if product["id"] == product_id), None)
        if target is None:
            raise KeyError("product not found")

        if action == "click":
            target["metrics"]["clicks"] += 1
        elif action == "positive":
            target["metrics"]["positive_feedback"] += 1
        elif action == "negative":
            target["metrics"]["negative_feedback"] += 1
        else:
            raise ValueError("invalid action")

        target["learned_score"] = compute_learned_score(target["metrics"])

        feedback.append(
            {
                "product_id": product_id,
                "action": action,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        )

        ranked = rank(products, tags=[], budget=0)
        rank_position = next((index + 1 for index, item in enumerate(ranked) if item["id"] == product_id), len(ranked))

        _record_metrics_unlocked(event=f"feedback:{action}", ranked_products=ranked)
        _persist_feedback_unlocked()
        _persist_products_unlocked()
        _persist_metrics_unlocked()

        return {
            "product": deepcopy(target),
            "rank_position": rank_position,
            "ranking": ranked,
        }

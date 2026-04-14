from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException

from backend.db.database import append_feedback, load_products, save_products
from backend.models.user import FeedbackRequest
from backend.utils.scoring import feedback_delta

router = APIRouter(tags=["feedback"])


@router.post("/feedback")
def feedback(payload: FeedbackRequest) -> dict:
    if payload.rating not in (-1, 1):
        raise HTTPException(status_code=400, detail="rating must be -1 or 1")

    products = load_products()

    for product in products:
        if product["id"] == payload.product_id:
            product["feedback_score"] = product.get("feedback_score", 0) + feedback_delta(payload.rating)

            record = {
                "product_id": payload.product_id,
                "rating": payload.rating,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
            append_feedback(record)
            save_products(products)

            return {
                "status": "ok",
                "updated_product": product,
            }

    raise HTTPException(status_code=404, detail="product not found")

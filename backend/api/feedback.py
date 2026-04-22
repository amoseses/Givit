from fastapi import APIRouter, HTTPException

from backend.db.database import record_feedback
from backend.models.user import FeedbackRequest

router = APIRouter(tags=["feedback"])


@router.post("/feedback")
def feedback(payload: FeedbackRequest) -> dict:
    try:
        result = record_feedback(payload.product_id, payload.action)
    except KeyError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error

    product = result["product"]
    rank_position = result["rank_position"]
    message = "This recommendation improved" if payload.action in {"click", "positive"} else "Feedback recorded"

    return {
        "status": "ok",
        "product_id": payload.product_id,
        "action": payload.action,
        "updated_score": product.get("learned_score", 0.0),
        "new_rank_position": rank_position,
        "message": message,
        "top_ranked": result["ranking"][:5],
    }

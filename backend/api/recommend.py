from fastapi import APIRouter

from backend.core.matcher import match_products
from backend.core.ranker import rank
from backend.core.tag_engine import extract_tags
from backend.db.database import load_products, track_recommendation_views
from backend.models.user import RecommendationRequest

router = APIRouter(tags=["recommend"])


@router.post("/recommend")
def recommend(payload: RecommendationRequest) -> dict:
    products = load_products()
    data = payload.model_dump()
    tags = extract_tags(data)
    matched = match_products(products, tags, payload.budget)
    ranked = rank(matched, tags=tags, budget=payload.budget)

    top_results = ranked[:5]
    track_recommendation_views([item["id"] for item in top_results], ranked)

    return {
        "query": data,
        "tags": tags,
        "results": top_results,
    }

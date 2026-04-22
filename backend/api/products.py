from fastapi import APIRouter

from backend.db.database import load_metrics, load_products

router = APIRouter(tags=["products"])


@router.get("/products")
def list_products() -> dict:
    return {"products": load_products()}


@router.get("/metrics")
def list_metrics() -> dict:
    return load_metrics()

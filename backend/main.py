from fastapi import FastAPI

from backend.api.feedback import router as feedback_router
from backend.api.products import router as products_router
from backend.api.recommend import router as recommend_router

app = FastAPI(title="Hive AI Gift Recommendation API", version="1.0.0")

app.include_router(products_router)
app.include_router(recommend_router)
app.include_router(feedback_router)


@app.get("/")
def health() -> dict:
    return {"status": "ok", "service": "hive-ai"}

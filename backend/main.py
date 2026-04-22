from fastapi import FastAPI

from backend.api.feedback import router as feedback_router
from backend.api.products import router as products_router
from backend.api.recommend import router as recommend_router
from backend.db.database import initialize_database

app = FastAPI(title="Hive AI Gift Recommendation API", version="2.0.0")


@app.on_event("startup")
def startup() -> None:
    initialize_database()


app.include_router(products_router)
app.include_router(recommend_router)
app.include_router(feedback_router)


@app.get("/")
def health() -> dict:
    return {"status": "ok", "service": "hive-ai"}

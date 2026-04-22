from pydantic import BaseModel, Field


class ProductMetrics(BaseModel):
    views: int = 0
    clicks: int = 0
    positive_feedback: int = 0
    negative_feedback: int = 0


class Product(BaseModel):
    id: int
    title: str
    tags: list[str] = Field(default_factory=list)
    price: float
    vendor: str
    popularity: int = 0
    metrics: ProductMetrics = Field(default_factory=ProductMetrics)
    learned_score: float = 0.0

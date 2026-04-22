from typing import Literal

from pydantic import BaseModel, Field


class RecommendationRequest(BaseModel):
    relationship: str | None = None
    interest: str | None = None
    interests: list[str] = Field(default_factory=list)
    budget: float
    occasion: str | None = None


class FeedbackRequest(BaseModel):
    product_id: int
    action: Literal["click", "positive", "negative"]

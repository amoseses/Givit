from pydantic import BaseModel, Field


class Product(BaseModel):
    id: int
    title: str
    tags: list[str] = Field(default_factory=list)
    price: float
    vendor: str
    popularity: int = 0
    feedback_score: int = 0
    score: float = 0

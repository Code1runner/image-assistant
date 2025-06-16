from typing import List, Optional
from pydantic import BaseModel, Field


class FAQItem(BaseModel):
    """Represents a single FAQ item with a question and its answer."""

    question: str = Field(..., description="The FAQ question")
    answer: str = Field(..., description="The answer to the FAQ question")
    embedding: Optional[List[float]] = Field(
        None, description="Embedding vector of the question"
    )


class VisionResponse(BaseModel):
    """Represents the response from the Vision API."""

    labels: List[str] = Field(
        ..., description="List of labels detected in the image"
    )
    objects: List[str] = Field(
        ..., description="List of objects detected in the image"
    )
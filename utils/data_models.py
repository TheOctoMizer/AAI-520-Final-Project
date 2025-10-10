"""Data models for the investment research system."""
from pydantic import BaseModel, Field
from typing import List, Optional


class Entity(BaseModel):
    """Named entity extracted from text."""
    text: str = Field(description="The extracted entity text")
    label: str = Field(description="Entity type (PERSON, ORGANIZATION, STOCK_SYMBOL, etc.)")
    confidence: Optional[float] = Field(description="Confidence score", default=None)


class NERResponse(BaseModel):
    """Named Entity Recognition response."""
    entities: List[Entity] = Field(description="List of extracted named entities")

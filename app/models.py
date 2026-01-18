"""
Pydantic schemas for normalized metadata.
"""

from pydantic import BaseModel
from typing import List, Optional


class Actor(BaseModel):
    name: str
    character: str


class WorkResponse(BaseModel):
    title: Optional[str]
    img_url: Optional[str]
    trailer_url: Optional[str]
    plot: Optional[str]
    rate: Optional[float]

    directors: List[str]
    writers: List[str]
    scenarios: List[str]
    actors: List[Actor]

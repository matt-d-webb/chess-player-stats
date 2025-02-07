from pydantic import BaseModel, Field
from typing import Optional, List

class Player(BaseModel):
    fide_id: int
    name: str
    country: str
    rating: Optional[int] = None
    title: Optional[str] = None
    birth_year: Optional[int] = None
    last_updated: Optional[str] = None

class PlayerResponse(BaseModel):
    status: str
    data: Optional[Player] = None
    error: Optional[str] = None

class PlayersListResponse(BaseModel):
    status: str
    data: List[Player] = []
    total: int = 0
    error: Optional[str] = None

class SearchParams(BaseModel):
    name: Optional[str] = None
    country: Optional[str] = None
    min_rating: Optional[int] = Field(None, ge=0, le=3000)
    title: Optional[str] = None
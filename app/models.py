from pydantic import BaseModel, Field
from typing import Optional, List

class Player(BaseModel):
    id: Optional[int] = None
    fide_id: int
    name: str
    country: str
    sex: Optional[str] = None
    title: Optional[str] = None
    w_title: Optional[str] = None
    o_title: Optional[str] = None
    foa_title: Optional[str] = None
    rating: Optional[float] = None
    games: Optional[float] = None
    k: Optional[float] = None
    rapid_rating: Optional[float] = None
    rapid_games: Optional[float] = None
    rapid_k: Optional[float] = None
    blitz_rating: Optional[float] = None
    blitz_games: Optional[float] = None
    blitz_k: Optional[float] = None
    birthday: Optional[float] = None
    flag: Optional[str] = None

    class Config:
        from_attributes = True

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
    min_rating: Optional[float] = Field(None, ge=0, le=3000)
    title: Optional[str] = None
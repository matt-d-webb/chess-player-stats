# app/routers/players.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from app import crud
from app.dependencies import get_db
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()

class Player(BaseModel):
    name: str
    rating: Optional[int]
    title: Optional[str]

class PlayerListResponse(BaseModel):
    country: str
    players: List[Player]

class CountryStats(BaseModel):
    country: str
    total_players: int
    avg_rating: float
    titled_players: int

class RatingDistribution(BaseModel):
    rating_range: str
    count: int

class DistributionResponse(BaseModel):
    distribution: List[RatingDistribution]
    country: str

@router.get("/player/{fide_id}")
def get_player(fide_id: int, db: Session = Depends(get_db)):
    player = crud.get_player(db, fide_id)
    if player is None:
        raise HTTPException(status_code=404, detail="Player not found")
    return player

@router.get("/search/")
def search_players(
    name: Optional[str] = None,
    country: Optional[str] = None,
    min_rating: Optional[int] = Query(None, ge=0, le=3000),
    title: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    players = crud.search_players(
        db, name=name, country=country,
        min_rating=min_rating, title=title,
        skip=skip, limit=limit
    )
    return {"players": players, "count": len(players)}

@router.get("/country/{country}/top", response_model=PlayerListResponse)
def get_top_players_by_country(
    country: str,
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    return crud.get_top_players_by_country(db, country.upper(), limit)

@router.get("/country/{country}/stats", response_model=CountryStats)
def get_country_stats(country: str, db: Session = Depends(get_db)):
    return crud.get_country_stats(db, country.upper())

@router.get("/rating-distribution", response_model=DistributionResponse)
def get_rating_distribution(
    country: Optional[str] = None,
    db: Session = Depends(get_db)
):
    return crud.get_rating_distribution(db, country.upper() if country else None)

@router.get("/titled-players/stats")
def get_titled_players_stats(db: Session = Depends(get_db)):
    return crud.get_titled_players_stats(db)
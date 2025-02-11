from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from app import crud
from app.dependencies import get_db
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()

class Player(BaseModel):
    name: str
    rating: Optional[int]
    title: Optional[str]
    country: str

class PlayerListResponse(BaseModel):
    players: List[Player]
    count: int

@router.get("/search/", response_model=PlayerListResponse)
async def search_players(
    name: Optional[str] = None,
    country: Optional[str] = None,
    min_rating: Optional[int] = Query(None, ge=0, le=3000),
    title: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    try:
        players = crud.search_players(
            db, 
            name=name, 
            country=country,
            min_rating=min_rating, 
            title=title,
            skip=skip, 
            limit=limit
        )
        return PlayerListResponse(players=players, count=len(players))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/player/{fide_id}")
async def get_player(fide_id: int, db: Session = Depends(get_db)):
    try:
        player = crud.get_player(db, fide_id)
        if player is None:
            raise HTTPException(status_code=404, detail="Player not found")
        return player
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/country/{country}/top", response_model=PlayerListResponse)
async def get_top_players_by_country(
    country: str,
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    try:
        result = crud.get_top_players_by_country(db, country.upper(), limit)
        return PlayerListResponse(
            players=result['players'],
            count=len(result['players'])
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/country/{country}/stats")
async def get_country_stats(country: str, db: Session = Depends(get_db)):
    try:
        return crud.get_country_stats(db, country.upper())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/rating-distribution")
async def get_rating_distribution(
    country: Optional[str] = None,
    db: Session = Depends(get_db)
):
    try:
        return crud.get_rating_distribution(db, country.upper() if country else None)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/titled-players/stats")
async def get_titled_players_stats(db: Session = Depends(get_db)):
    try:
        return crud.get_titled_players_stats(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
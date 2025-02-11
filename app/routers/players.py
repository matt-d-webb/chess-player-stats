# app/routers/players.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from app import crud
from app.dependencies import get_db
from app.models import PlayerResponse, PlayersListResponse, SearchParams

router = APIRouter()

@router.get("/search/", response_model=PlayersListResponse)
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
        search_params = SearchParams(
            name=name,
            country=country,
            min_rating=min_rating,
            title=title
        )
        players = crud.search_players(db, search_params, skip, limit)
        return PlayersListResponse(
            status="success",
            data=players,
            total=len(players)
        )
    except Exception as e:
        return PlayersListResponse(
            status="error",
            error=str(e)
        )

@router.get("/player/{fide_id}", response_model=PlayerResponse)
async def get_player(fide_id: int, db: Session = Depends(get_db)):
    try:
        player = crud.get_player(db, fide_id)
        if player is None:
            return PlayerResponse(
                status="error",
                error=f"Player with FIDE ID {fide_id} not found"
            )
        return PlayerResponse(status="success", data=player)
    except Exception as e:
        return PlayerResponse(status="error", error=str(e))

@router.get("/country/{country}/top", response_model=PlayersListResponse)
async def get_top_players_by_country(
    country: str,
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    try:
        players = crud.get_top_players_by_country(db, country.upper(), limit)
        return PlayersListResponse(
            status="success",
            data=players,
            total=len(players)
        )
    except Exception as e:
        return PlayersListResponse(
            status="error",
            error=str(e)
        )

@router.get("/country/{country}/stats")
async def get_country_stats(country: str, db: Session = Depends(get_db)):
    try:
        stats = crud.get_country_stats(db, country.upper())
        return {"status": "success", "data": stats}
    except Exception as e:
        return {"status": "error", "error": str(e)}

@router.get("/rating-distribution")
async def get_rating_distribution(
    country: Optional[str] = None,
    db: Session = Depends(get_db)
):
    try:
        distribution = crud.get_rating_distribution(db, country.upper() if country else None)
        return {"status": "success", "data": distribution}
    except Exception as e:
        return {"status": "error", "error": str(e)}

@router.get("/titled-players/stats")
async def get_titled_players_stats(db: Session = Depends(get_db)):
    try:
        stats = crud.get_titled_players_stats(db)
        return {"status": "success", "data": stats}
    except Exception as e:
        return {"status": "error", "error": str(e)}
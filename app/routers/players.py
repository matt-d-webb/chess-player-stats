from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import Optional, List
from app.database import PlayerDB
from app.dependencies import get_db, cache

router = APIRouter()

@router.get("/federation/{federation}/stats")
def get_federation_stats(federation: str, db: Session = Depends(get_db)):
    cache_key = f"fed_stats_{federation}"
    cached = cache.get(cache_key)
    if cached:
        return cached

    stats = db.query(
        func.count().label('total_players'),
        func.avg(func.nullif(PlayerDB.standard_rating, 0)).label('avg_rating'),
        func.count(PlayerDB.title).label('titled_players')
    ).filter(
        PlayerDB.federation == federation,
        PlayerDB.standard_rating.isnot(None)
    ).first()

    result = {
        'federation': federation,
        'total_players': int(stats[0]),
        'avg_rating': round(float(stats[1] or 0), 2),
        'titled_players': int(stats[2])
    }
    
    cache.set(cache_key, result)
    return result

@router.get("/rating-distribution")
def get_rating_distribution(
    federation: Optional[str] = None,
    db: Session = Depends(get_db)
):
    cache_key = f"rating_dist_{federation or 'all'}"
    cached = cache.get(cache_key)
    if cached:
        return cached

    query = db.query(
        func.floor(PlayerDB.standard_rating/100)*100,
        func.count()
    ).filter(PlayerDB.standard_rating > 0)

    if federation:
        query = query.filter(PlayerDB.federation == federation)

    distribution = query.group_by(
        func.floor(PlayerDB.standard_rating/100)*100
    ).order_by(
        func.floor(PlayerDB.standard_rating/100)*100
    ).all()

    result = {
        'distribution': [{'rating_range': f"{int(r[0])}-{int(r[0])+99}", 'count': r[1]} 
                        for r in distribution],
        'federation': federation or 'all'
    }
    
    cache.set(cache_key, result)
    return result

@router.get("/federation/{federation}/top")
def get_top_players_by_federation(
    federation: str,
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    cache_key = f"top_players_{federation}_{limit}"
    cached = cache.get(cache_key)
    if cached:
        return cached

    players = db.query(PlayerDB).filter(
        PlayerDB.federation == federation,
        PlayerDB.standard_rating > 0
    ).order_by(
        desc(PlayerDB.standard_rating)
    ).limit(limit).all()

    result = {
        'federation': federation,
        'players': [
            {
                'name': p.name,
                'rating': p.standard_rating,
                'title': p.title
            } for p in players
        ]
    }
    
    cache.set(cache_key, result)
    return result

@router.get("/titled-players/stats")
def get_titled_players_stats(db: Session = Depends(get_db)):
    cache_key = "titled_players_stats"
    cached = cache.get(cache_key)
    if cached:
        return cached

    stats = db.query(
        PlayerDB.federation,
        PlayerDB.title,
        func.count()
    ).filter(
        PlayerDB.title.isnot(None),
        PlayerDB.title != ''
    ).group_by(
        PlayerDB.federation,
        PlayerDB.title
    ).all()

    result = {}
    for federation, title, count in stats:
        if federation not in result:
            result[federation] = {}
        result[federation][title] = count

    cache.set(cache_key, result)
    return result
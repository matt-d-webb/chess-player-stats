from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import List, Optional
from app.database import PlayerDB
from app.dependencies import cache

def get_player(db: Session, fide_id: int):
    return db.query(PlayerDB).filter(PlayerDB.fide_id == fide_id).first()

def search_players(
    db: Session,
    name: Optional[str] = None,
    country: Optional[str] = None,
    min_rating: Optional[int] = None,
    title: Optional[str] = None,
    skip: int = 0,
    limit: int = 100
):
    query = db.query(PlayerDB)
    
    if name:
        query = query.filter(PlayerDB.name.ilike(f"%{name}%"))
    if country:
        query = query.filter(PlayerDB.country == country.upper())
    if min_rating:
        query = query.filter(PlayerDB.rating >= min_rating)
    if title:
        query = query.filter(PlayerDB.title == title.upper())
    
    return query.offset(skip).limit(limit).all()

def get_top_players_by_country(db: Session, country: str, limit: int = 10):
    cache_key = f"top_players_{country}_{limit}"
    cached = cache.get(cache_key)
    if cached:
        return cached

    players = db.query(PlayerDB).filter(
        PlayerDB.country == country,
        PlayerDB.rating.isnot(None)
    ).order_by(
        desc(PlayerDB.rating)
    ).limit(limit).all()

    result = {
        'country': country,
        'players': [
            {
                'name': p.name,
                'rating': p.rating,
                'title': p.title
            } for p in players
        ]
    }
    
    cache.set(cache_key, result)
    return result

def get_country_stats(db: Session, country: str):
    cache_key = f"country_stats_{country}"
    cached = cache.get(cache_key)
    if cached:
        return cached

    stats = db.query(
        func.count().label('total_players'),
        func.avg(func.nullif(PlayerDB.rating, 0)).label('avg_rating'),
        func.count(PlayerDB.title).label('titled_players')
    ).filter(
        PlayerDB.country == country,
        PlayerDB.rating.isnot(None)
    ).first()

    result = {
        'country': country,
        'total_players': int(stats[0]),
        'avg_rating': round(float(stats[1] or 0), 2),
        'titled_players': int(stats[2])
    }
    
    cache.set(cache_key, result)
    return result

def get_rating_distribution(db: Session, country: Optional[str] = None):
    cache_key = f"rating_dist_{country or 'all'}"
    cached = cache.get(cache_key)
    if cached:
        return cached

    query = db.query(
        func.floor(PlayerDB.rating/100)*100,
        func.count()
    ).filter(PlayerDB.rating.isnot(None))

    if country:
        query = query.filter(PlayerDB.country == country)

    distribution = query.group_by(
        func.floor(PlayerDB.rating/100)*100
    ).order_by(
        func.floor(PlayerDB.rating/100)*100
    ).all()

    result = {
        'distribution': [{'rating_range': f"{int(r[0])}-{int(r[0])+99}", 'count': r[1]} 
                        for r in distribution],
        'country': country or 'all'
    }
    
    cache.set(cache_key, result)
    return result

def get_titled_players_stats(db: Session):
    cache_key = "titled_players_stats"
    cached = cache.get(cache_key)
    if cached:
        return cached

    stats = db.query(
        PlayerDB.country,
        PlayerDB.title,
        func.count()
    ).filter(
        PlayerDB.title.isnot(None),
        PlayerDB.title != ''
    ).group_by(
        PlayerDB.country,
        PlayerDB.title
    ).all()

    result = {}
    for country, title, count in stats:
        if country not in result:
            result[country] = {}
        result[country][title] = count

    cache.set(cache_key, result)
    return result
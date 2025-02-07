from sqlalchemy import func, desc, and_
from sqlalchemy.orm import Session
from typing import List, Optional, Dict
from . import models, database
from .cache import cache
import json

def get_federation_stats(db: Session, federation: str):
    cache_key = f"fed_stats_{federation}"
    cached = cache.get(cache_key)
    if cached:
        return cached

    stats = db.query(
        func.count().label('total_players'),
        func.avg(database.PlayerDB.standard_rating).label('avg_rating'),
        func.count(database.PlayerDB.title).label('titled_players')
    ).filter(
        database.PlayerDB.federation == federation,
        database.PlayerDB.standard_rating > 0
    ).first()

    result = {
        'federation': federation,
        'total_players': int(stats[0]),
        'avg_rating': round(float(stats[1] or 0), 2),
        'titled_players': int(stats[2])
    }
    
    cache.set(cache_key, result)
    return result

def get_rating_distribution(db: Session, federation: Optional[str] = None):
    cache_key = f"rating_dist_{federation or 'all'}"
    cached = cache.get(cache_key)
    if cached:
        return cached

    query = db.query(
        func.floor(database.PlayerDB.standard_rating/100)*100,
        func.count()
    ).filter(database.PlayerDB.standard_rating > 0)

    if federation:
        query = query.filter(database.PlayerDB.federation == federation)

    distribution = query.group_by(
        func.floor(database.PlayerDB.standard_rating/100)*100
    ).order_by(
        func.floor(database.PlayerDB.standard_rating/100)*100
    ).all()

    result = {
        'distribution': [{'rating_range': f"{int(r[0])}-{int(r[0])+99}", 'count': r[1]} 
                        for r in distribution],
        'federation': federation or 'all'
    }
    
    cache.set(cache_key, result)
    return result

def get_top_players_by_federation(db: Session, federation: str, limit: int = 10):
    cache_key = f"top_players_{federation}_{limit}"
    cached = cache.get(cache_key)
    if cached:
        return cached

    players = db.query(database.PlayerDB).filter(
        database.PlayerDB.federation == federation,
        database.PlayerDB.standard_rating > 0
    ).order_by(
        desc(database.PlayerDB.standard_rating)
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

def get_titled_players_stats(db: Session):
    cache_key = "titled_players_stats"
    cached = cache.get(cache_key)
    if cached:
        return cached

    stats = db.query(
        database.PlayerDB.federation,
        database.PlayerDB.title,
        func.count()
    ).filter(
        database.PlayerDB.title.isnot(None),
        database.PlayerDB.title != ''
    ).group_by(
        database.PlayerDB.federation,
        database.PlayerDB.title
    ).all()

    result = {}
    for federation, title, count in stats:
        if federation not in result:
            result[federation] = {}
        result[federation][title] = count

    cache.set(cache_key, result)
    return result
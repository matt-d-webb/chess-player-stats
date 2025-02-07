# app/dependencies.py
from app.database import SessionLocal
import time

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class TTLCache:
    def __init__(self, ttl_seconds=3600):
        self.cache = {}
        self.ttl = ttl_seconds

    def get(self, key):
        if key in self.cache:
            value, timestamp = self.cache[key]
            if timestamp + self.ttl > time.time():
                return value
            del self.cache[key]
        return None

    def set(self, key, value):
        self.cache[key] = (value, time.time())

cache = TTLCache()
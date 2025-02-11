# app/config.py
from pydantic import BaseModel
from typing import Optional, List

class Settings(BaseModel):
    # Database settings
    DATABASE_URL: str = "postgresql://matthew@localhost/chess_players"
    
    # API settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Chess Stats API"
    
    # CORS settings
    BACKEND_CORS_ORIGINS: List[str] = ["*"]
    
    # Production settings
    DEBUG: bool = False
    
    # Optional API key auth
    API_KEY: Optional[str] = None
    
    class Config:
        env_file = ".env"

settings = Settings()
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Database settings
    DATABASE_URL: str = "postgresql://matthew@localhost/chess_players"
    
    # API settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Chess Stats API"
    
    # CORS settings
    BACKEND_CORS_ORIGINS: list = ["*"]
    
    # Production settings
    DEBUG: bool = False
    
    # Optional API key auth
    API_KEY: Optional[str] = None
    
    class Config:
        env_file = ".env"

settings = Settings()
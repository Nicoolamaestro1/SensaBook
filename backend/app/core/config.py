from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "SensaBook API"
    API_VERSION: str = "v1"
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/sensabook"
    
    # JWT Settings
    SECRET_KEY: str = "your-secret-key-here"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Redis Settings
    REDIS_URL: str = "redis://localhost:6379"
    
    # AI Model Settings
    SPACY_MODEL: str = "en_core_web_sm"
    EMOTION_ANALYSIS_ENABLED: bool = True
    SOUNDSCAPE_GENERATION_ENABLED: bool = True
    
    # Audio Settings
    AUDIO_CACHE_TTL: int = 3600  # 1 hour
    MAX_AUDIO_FILE_SIZE: int = 50 * 1024 * 1024  # 50MB
    
    # Performance Settings
    CACHE_ENABLED: bool = True
    ANALYTICS_ENABLED: bool = True
    
    # CORS Settings
    ALLOWED_ORIGINS: list = ["http://localhost:3000", "http://localhost:8081"]

    class Config:
        env_file = ".env"

settings = Settings()
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Shared configuration settings"""
    
    # App
    APP_NAME: str = "Health Management Platform"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # Database
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/health_platform"
    
    # JWT
    SECRET_KEY: str = "your-secret-key-change-this-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Service URLs (for inter-service communication)
    AUTH_SERVICE_URL: str = "http://auth-service:8001"
    USER_SERVICE_URL: str = "http://user-service:8002"
    HEALTH_DATA_SERVICE_URL: str = "http://health-data-service:8003"
    AI_SERVICE_URL: str = "http://ai-service:8004"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()


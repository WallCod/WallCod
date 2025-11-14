"""
Application configuration module.
"""
from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl, validator


class Settings(BaseSettings):
    """Application settings."""

    # Application
    APP_NAME: str = "WallCod Portfolio API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    ENVIRONMENT: str = "development"

    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # Database
    DATABASE_URL: str
    DATABASE_POOL_SIZE: int = 10
    DATABASE_MAX_OVERFLOW: int = 20

    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # CORS
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]
    ALLOWED_METHODS: List[str] = ["GET", "POST", "PUT", "DELETE", "PATCH"]
    ALLOWED_HEADERS: List[str] = ["*"]

    @validator("ALLOWED_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v):
        if isinstance(v, str):
            return [i.strip() for i in v.split(",")]
        return v

    @validator("ALLOWED_METHODS", pre=True)
    def assemble_cors_methods(cls, v):
        if isinstance(v, str):
            return [i.strip() for i in v.split(",")]
        return v

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    CACHE_TTL: int = 300

    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    RATE_LIMIT_PER_HOUR: int = 1000

    # Sentry
    SENTRY_DSN: Optional[str] = None

    # Email
    SMTP_HOST: Optional[str] = None
    SMTP_PORT: Optional[int] = None
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    SMTP_FROM: Optional[str] = None

    # API Keys
    GITHUB_TOKEN: Optional[str] = None
    LINKEDIN_API_KEY: Optional[str] = None

    # Feature Flags
    ENABLE_REGISTRATION: bool = True
    ENABLE_EMAIL_VERIFICATION: bool = False
    ENABLE_SWAGGER_UI: bool = True

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

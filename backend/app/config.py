"""
Application Configuration
Loads settings from environment variables with sensible defaults.
"""

from pydantic import field_validator
from pydantic_settings import BaseSettings
from typing import Any, List


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Gemini API Configuration
    gemini_api_key: str = ""
    gemini_model: str = "gemini-2.0-flash"
    gemini_timeout: int = 60  # seconds
    
    # Server Configuration
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = True
    
    # CORS Configuration
    cors_origins: str = "http://localhost:3000,http://127.0.0.1:3000"
    
    # Data Paths
    colleges_csv_path: str = "app/data/colleges.csv"
    careers_csv_path: str = "app/data/career_recommender.csv"
    model_path: str = "app/models/xgboost_model.pkl"
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS origins from comma-separated string."""
        return [origin.strip() for origin in self.cors_origins.split(",")]

    @field_validator("debug", mode="before")
    @classmethod
    def parse_debug_mode(cls, value: Any) -> Any:
        """Accept boolean-like values plus deployment mode names."""
        if isinstance(value, str):
            normalized = value.strip().lower()
            if normalized in {"true", "1", "yes", "y", "on", "debug", "dev", "development", "local"}:
                return True
            if normalized in {"false", "0", "no", "n", "off", "release", "prod", "production"}:
                return False
        return value
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Global settings instance
settings = Settings()

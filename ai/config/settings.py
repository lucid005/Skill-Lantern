"""
Skill Lantern AI - Application Settings
"""

from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Optional
import os


class Settings(BaseSettings):
    """Application configuration settings"""
    
    # Server
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = True
    environment: str = "development"
    
    # Database
    database_url: Optional[str] = None
    
    # API Keys (Optional - for LLM integration)
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    gemini_api_key: Optional[str] = None
    
    # Model Configuration
    model_path: str = "./models/trained"
    use_gpu: bool = False
    
    # CORS
    frontend_url: str = "http://localhost:3000"
    
    # Paths
    careers_config_path: str = "./config/careers.yaml"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()


# Export settings instance
settings = get_settings()

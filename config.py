"""
Application configuration settings.
"""
import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    """Application settings."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    # Database (using Supabase REST API - no direct connection needed)
    
    # Authentication
    jwt_secret: str
    jwt_algorithm: str = "HS256"
    jwt_expiration_hours: int = 24
    
    # External APIs
    spotify_client_id: str
    spotify_client_secret: str
    supabase_url: str
    supabase_key: str
    
    # Application
    app_name: str = "Ekubo API"
    debug: bool = False


# Create settings instance
settings = Settings()

# Validate required settings

if not settings.jwt_secret:
    raise ValueError("JWT_SECRET environment variable is required")

if not settings.spotify_client_id:
    raise ValueError("SPOTIFY_CLIENT_ID environment variable is required")

if not settings.spotify_client_secret:
    raise ValueError("SPOTIFY_CLIENT_SECRET environment variable is required")

if not settings.supabase_url:
    raise ValueError("SUPABASE_URL environment variable is required")

if not settings.supabase_key:
    raise ValueError("SUPABASE_KEY environment variable is required")

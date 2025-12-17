"""
Configuration management for PowerMem API Server
"""

import os
from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import Field, ConfigDict


class ServerConfig(BaseSettings):
    """Server configuration settings"""
    
    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",  # Ignore extra fields from .env that are not in this model
    )
    
    # Server settings
    host: str = Field(default="0.0.0.0", env="POWERMEM_SERVER_HOST")
    port: int = Field(default=8000, env="POWERMEM_SERVER_PORT")
    workers: int = Field(default=4, env="POWERMEM_SERVER_WORKERS")
    reload: bool = Field(default=False, env="POWERMEM_SERVER_RELOAD")
    
    # Authentication settings
    auth_enabled: bool = Field(default=True, env="POWERMEM_AUTH_ENABLED")
    api_keys: str = Field(default="", env="POWERMEM_API_KEYS")
    
    # Rate limiting settings
    rate_limit_enabled: bool = Field(default=True, env="POWERMEM_RATE_LIMIT_ENABLED")
    rate_limit_per_minute: int = Field(default=100, env="POWERMEM_RATE_LIMIT_PER_MINUTE")
    
    # Logging settings
    log_level: str = Field(default="INFO", env="POWERMEM_LOG_LEVEL")
    log_format: str = Field(default="json", env="POWERMEM_LOG_FORMAT")  # json or text
    
    # API settings
    api_title: str = Field(default="PowerMem API", env="POWERMEM_API_TITLE")
    api_version: str = Field(default="v1", env="POWERMEM_API_VERSION")
    api_description: str = Field(
        default="PowerMem HTTP API Server - Intelligent Memory System",
        env="POWERMEM_API_DESCRIPTION"
    )
    
    # CORS settings
    cors_enabled: bool = Field(default=True, env="POWERMEM_CORS_ENABLED")
    cors_origins: str = Field(default="*", env="POWERMEM_CORS_ORIGINS")
    
    def get_api_keys_list(self) -> List[str]:
        """Get list of valid API keys"""
        if not self.api_keys:
            return []
        return [key.strip() for key in self.api_keys.split(",") if key.strip()]
    
    def get_cors_origins_list(self) -> List[str]:
        """Get list of CORS origins"""
        if self.cors_origins == "*":
            return ["*"]
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


# Global config instance
config = ServerConfig()

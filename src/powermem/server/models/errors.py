"""
Error codes and exception classes for PowerMem API
"""

from enum import Enum
from typing import Any, Dict, Optional


class ErrorCode(str, Enum):
    """Error codes for API responses"""
    
    # General errors
    INTERNAL_ERROR = "INTERNAL_ERROR"
    INVALID_REQUEST = "INVALID_REQUEST"
    UNAUTHORIZED = "UNAUTHORIZED"
    FORBIDDEN = "FORBIDDEN"
    NOT_FOUND = "NOT_FOUND"
    RATE_LIMIT_EXCEEDED = "RATE_LIMIT_EXCEEDED"
    
    # Memory errors
    MEMORY_NOT_FOUND = "MEMORY_NOT_FOUND"
    MEMORY_CREATE_FAILED = "MEMORY_CREATE_FAILED"
    MEMORY_UPDATE_FAILED = "MEMORY_UPDATE_FAILED"
    MEMORY_DELETE_FAILED = "MEMORY_DELETE_FAILED"
    
    # Search errors
    SEARCH_FAILED = "SEARCH_FAILED"
    INVALID_SEARCH_PARAMS = "INVALID_SEARCH_PARAMS"
    
    # User errors
    USER_NOT_FOUND = "USER_NOT_FOUND"
    PROFILE_UPDATE_FAILED = "PROFILE_UPDATE_FAILED"
    
    # Agent errors
    AGENT_NOT_FOUND = "AGENT_NOT_FOUND"
    AGENT_MEMORY_SHARE_FAILED = "AGENT_MEMORY_SHARE_FAILED"
    
    # Configuration errors
    CONFIG_ERROR = "CONFIG_ERROR"
    STORAGE_ERROR = "STORAGE_ERROR"


class APIError(Exception):
    """Base exception for API errors"""
    
    def __init__(
        self,
        code: ErrorCode,
        message: str,
        details: Optional[Dict[str, Any]] = None,
        status_code: int = 500,
    ):
        self.code = code
        self.message = message
        self.details = details or {}
        self.status_code = status_code
        super().__init__(self.message)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert error to dictionary"""
        return {
            "code": self.code.value,
            "message": self.message,
            "details": self.details,
        }

"""
Error handling middleware for PowerMem API
"""

import logging
from typing import Union
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from ..models.errors import ErrorCode, APIError
from ..models.response import ErrorResponse
from datetime import datetime

logger = logging.getLogger("server")


async def error_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Global error handler for FastAPI application.
    
    Args:
        request: FastAPI request object
        exc: Exception that was raised
        
    Returns:
        JSONResponse with error details
    """
    # Handle APIError
    if isinstance(exc, APIError):
        error_response = ErrorResponse(
            error=exc.to_dict(),
            timestamp=datetime.utcnow(),
        )
        return JSONResponse(
            status_code=exc.status_code,
            content=error_response.model_dump(),
        )
    
    # Handle HTTPException
    if isinstance(exc, StarletteHTTPException):
        error_detail = exc.detail
        if isinstance(error_detail, dict):
            error_code = error_detail.get("code", ErrorCode.INTERNAL_ERROR.value)
            error_message = error_detail.get("message", str(exc))
        else:
            error_code = ErrorCode.INTERNAL_ERROR.value
            error_message = str(error_detail)
        
        error_response = ErrorResponse(
            error={
                "code": error_code,
                "message": error_message,
                "details": {},
            },
            timestamp=datetime.utcnow(),
        )
        return JSONResponse(
            status_code=exc.status_code,
            content=error_response.model_dump(),
        )
    
    # Handle validation errors
    if isinstance(exc, RequestValidationError):
        error_response = ErrorResponse(
            error={
                "code": ErrorCode.INVALID_REQUEST.value,
                "message": "Request validation failed",
                "details": {
                    "errors": exc.errors(),
                },
            },
            timestamp=datetime.utcnow(),
        )
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=error_response.model_dump(),
        )
    
    # Handle unexpected errors
    logger.exception(f"Unhandled error: {exc}")
    error_response = ErrorResponse(
        error={
            "code": ErrorCode.INTERNAL_ERROR.value,
            "message": "Internal server error",
            "details": {},
        },
        timestamp=datetime.utcnow(),
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=error_response.model_dump(),
    )

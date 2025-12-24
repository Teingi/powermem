"""
System management API routes
"""

from fastapi import APIRouter, Depends, Request, Response
from slowapi import Limiter

from ...models.response import APIResponse, HealthResponse, StatusResponse
from ...middleware.auth import verify_api_key
from ...middleware.rate_limit import limiter, get_rate_limit_string
from ...config import config
from ...utils.metrics import get_metrics_collector
from powermem import auto_config

router = APIRouter(prefix="/system", tags=["system"])


@router.get(
    "/health",
    response_model=APIResponse,
    summary="Health check",
    description="Check if the API server is healthy (public endpoint, no authentication required)",
)
async def health_check():
    """Health check endpoint"""
    health = HealthResponse(status="healthy")
    
    return APIResponse(
        success=True,
        data=health.model_dump(mode='json'),
        message="Service is healthy",
    )


@router.get(
    "/status",
    response_model=APIResponse,
    summary="System status",
    description="Get system status and configuration information",
)
@limiter.limit(get_rate_limit_string())
async def get_status(
    request: Request,
    api_key: str = Depends(verify_api_key),
):
    """Get system status"""
    # Get PowerMem config
    powermem_config = auto_config()
    
    storage_type = None
    llm_provider = None
    
    if isinstance(powermem_config, dict):
        # Extract from dict config
        vector_store = powermem_config.get("vector_store") or powermem_config.get("database", {})
        storage_type = vector_store.get("provider") if isinstance(vector_store, dict) else None
        
        llm = powermem_config.get("llm", {})
        llm_provider = llm.get("provider") if isinstance(llm, dict) else None
    else:
        # Extract from config object
        if hasattr(powermem_config, "vector_store") and powermem_config.vector_store:
            storage_type = powermem_config.vector_store.provider
        if hasattr(powermem_config, "llm") and powermem_config.llm:
            llm_provider = powermem_config.llm.provider
    
    status_data = StatusResponse(
        status="operational",
        version=config.api_version,
        storage_type=storage_type,
        llm_provider=llm_provider,
    )
    
    return APIResponse(
        success=True,
        data=status_data.model_dump(mode='json'),
        message="System status retrieved successfully",
    )


@router.get(
    "/metrics",
    summary="Prometheus metrics",
    description="Get Prometheus format metrics",
)
@limiter.limit(get_rate_limit_string())
async def get_metrics(
    request: Request,
    api_key: str = Depends(verify_api_key),
):
    """Get Prometheus format metrics"""
    metrics_collector = get_metrics_collector()
    metrics_text = metrics_collector.get_metrics()
    
    return Response(
        content=metrics_text,
        media_type="text/plain; version=0.0.4; charset=utf-8"
    )


@router.post(
    "/reset",
    response_model=APIResponse,
    summary="Reset all memories",
    description="Reset all memories (requires admin permissions - placeholder)",
)
@limiter.limit(get_rate_limit_string())
async def reset_memories(
    request: Request,
    api_key: str = Depends(verify_api_key),
):
    """Reset all memories"""
    # Placeholder implementation
    # In production, this would require admin permissions and actually reset the memory store
    from powermem import Memory
    
    try:
        memory = Memory(config=auto_config())
        memory.reset()
        
        return APIResponse(
            success=True,
            data={},
            message="All memories reset successfully",
        )
    except Exception as e:
        from ...models.errors import ErrorCode, APIError
        raise APIError(
            code=ErrorCode.INTERNAL_ERROR,
            message=f"Failed to reset memories: {str(e)}",
            status_code=500,
        )

"""
Health check endpoints
"""

from fastapi import APIRouter
from datetime import datetime

router = APIRouter()


@router.get("/health")
async def health_check():
    """Check API health status"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "skill-lantern-ai",
    }


@router.get("/health/ready")
async def readiness_check():
    """Check if the service is ready to accept requests"""
    return {
        "ready": True,
        "timestamp": datetime.utcnow().isoformat(),
    }

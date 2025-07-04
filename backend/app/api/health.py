from fastapi import APIRouter
import os
import sys

router = APIRouter()

@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

@router.get("/debug")
async def debug_info():
    """Debug endpoint to verify API functionality."""
    return {
        "environment": os.environ.get("ENVIRONMENT", "development"),
        "python_version": sys.version,
        "allowed_hosts": os.environ.get("ALLOWED_HOSTS", ""),
        "database": os.environ.get("DATABASE_URL", ""),
        "api_working": True
    }
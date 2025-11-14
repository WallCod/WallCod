"""
API v1 router configuration.
"""
from fastapi import APIRouter
from .endpoints import auth, users


api_router = APIRouter()

# Include endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])

from app.api.endpoints import books
from app.api.endpoints import analytics
from app.api import auth
from fastapi import APIRouter
from . import sample, soundscape

router = APIRouter()

# Core API endpoints
router.include_router(books.router, prefix="/api", tags=["books"])

# Authentication endpoints
router.include_router(auth.router, prefix="/auth", tags=["authentication"])

# Revolutionary analytics and emotion analysis endpoints
router.include_router(analytics.router, prefix="/api/analytics", tags=["analytics"])

# Legacy endpoints
router.include_router(sample.router)
router.include_router(soundscape.router)

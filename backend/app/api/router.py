from app.api.endpoints import books
from fastapi import APIRouter
from . import sample, soundscape

router = APIRouter()
router.include_router(books.router, prefix="/api", tags=["books"])
router.include_router(sample.router)
router.include_router(soundscape.router)

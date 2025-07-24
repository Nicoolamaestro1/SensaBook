from fastapi import APIRouter
from . import sample, book, soundscape

router = APIRouter()
router.include_router(sample.router)
router.include_router(book.router)
router.include_router(soundscape.router)
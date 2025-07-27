from fastapi import APIRouter
from app.api.endpoints import books

router = APIRouter()
router.include_router(books.router, prefix="/api", tags=["books"])
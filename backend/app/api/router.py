from fastapi import APIRouter
from .endpoints import books, analytics
from .simple_soundscape import router as simple_soundscape_router

api_router = APIRouter()

# Include the new simple soundscape router
api_router.include_router(simple_soundscape_router, tags=["simple-soundscape"])

# Include other endpoints
api_router.include_router(books.router, prefix="/books", tags=["books"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["analytics"])

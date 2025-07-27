from fastapi import APIRouter
from app.services.soundscape import get_ambient_soundscape

router = APIRouter(prefix="/soundscape", tags=["Soundscape"])

@router.get("/book/{book_id}")
def get_soundscape(book_id: int):
    return get_ambient_soundscape(book_id)
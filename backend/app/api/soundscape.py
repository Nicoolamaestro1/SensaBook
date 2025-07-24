from fastapi import APIRouter
from app.services.soundscape import get_soundscape_for_book

router = APIRouter(prefix="/soundscape", tags=["Soundscape"])

@router.get("/book/{book_id}")
def get_soundscape(book_id: int):
    return get_soundscape_for_book(book_id)
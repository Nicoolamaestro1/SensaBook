from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.services.soundscape import get_ambient_soundscape
from app.db.session import get_db

router = APIRouter(prefix="/soundscape", tags=["Soundscape"])

@router.get("/book_page/{book_page_id}")
def get_soundscape(book_id: int, book_page_id: int, db: Session = Depends(get_db)):
    return get_ambient_soundscape(book_id, book_page_id, db)
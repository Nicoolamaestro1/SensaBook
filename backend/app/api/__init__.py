from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.book import Book
from . import sample, soundscape

router = APIRouter()
router.include_router(sample.router)
router.include_router(soundscape.router)

@router.post("/book")
def create_book(title: str, chapters: list[str], db: Session = Depends(get_db)):
    book = Book(title=title, chapters=chapters)
    db.add(book)
    db.commit()
    db.refresh(book)
    return book

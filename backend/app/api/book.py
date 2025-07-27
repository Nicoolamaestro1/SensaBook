from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services import book as book_service
from app.models.book import Book
from pydantic import BaseModel

router = APIRouter(prefix="/books", tags=["Books"])

class BookCreate(BaseModel):
    title: str
    author: str | None = None
    summary: str | None = None
    cover_url: str | None = None
    genre: str | None = None
    content: str

@router.get("/")
def read_books(db: Session = Depends(get_db)):
    return book_service.get_books(db)

@router.get("/{book_id}")
def read_book(book_id: int, db: Session = Depends(get_db)):
    book = book_service.get_book(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.post("/book")
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    db_book = Book(
        title=book.title,
        author=book.author,
        summary=book.summary,
        cover_url=book.cover_url,
        genre=book.genre,
        content=book.content
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book
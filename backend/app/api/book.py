from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services import book as book_service

router = APIRouter(prefix="/books", tags=["Books"])

@router.get("/")
def read_books(db: Session = Depends(get_db)):
    return book_service.get_books(db)

@router.get("/{book_id}")
def read_book(book_id: int, db: Session = Depends(get_db)):
    book = book_service.get_book(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book
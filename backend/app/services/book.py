from sqlalchemy.orm import Session
from app.models.book import Book

def get_books(db: Session):
    return db.query(Book).all()

def get_book(db: Session, book_id: int):
    return db.query(Book).filter(Book.id == book_id).first()

def create_book(db: Session, book_data: dict):
    book = Book(**book_data)
    db.add(book)
    db.commit()
    db.refresh(book)
    return book
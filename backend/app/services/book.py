from sqlalchemy.orm import Session
from app.models.book import Book
from app.models.book import BookPage

def get_books(db: Session):
    return db.query(Book).all()

def get_book(book_id: int, db: Session):
    return db.query(Book).filter(Book.id == book_id).first()

def get_book_page(book_page_id: int, book_id: int, db: Session):
    return db.query(BookPage).filter(book_id == book_id, BookPage.id == book_page_id).first()

def create_book(db: Session, book_data: dict):
    book = Book(**book_data)
    db.add(book)
    db.commit()
    db.refresh(book)
    return book
from sqlalchemy.orm import Session
from app.models.book import Book, Chapter, Page

def get_books(db: Session):
    return db.query(Book).all()

def get_book(db: Session, book_id: int):
    return db.query(Book).filter(Book.id == book_id).first()

def get_chapter(db: Session, chapter_number: int, book_id: int):
    return db.query(Chapter).filter(Chapter.chapter_number == chapter_number, Chapter.book_id == book_id).first()

def get_page(db: Session, book_id: int, chapter_number: int, page_number: int):
    chapter = db.query(Chapter).filter(
        Chapter.book_id == book_id,
        Chapter.chapter_number == chapter_number
    ).first()
    if not chapter:
        return None
    page = db.query(Page).filter(
        Page.chapter_id == chapter.id,
        Page.page_number == page_number
    ).first()
    return page

def create_book(db: Session, book_data: dict):
    book = Book(**book_data)
    db.add(book)
    db.commit()
    db.refresh(book)
    return book
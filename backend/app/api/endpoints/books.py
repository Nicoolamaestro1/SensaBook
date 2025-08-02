from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from app.db.session import get_db
from app.models.book import Book, Chapter, Page
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()

# Pydantic modeli
class PageCreate(BaseModel):
    page_number: int
    content: str

class ChapterCreate(BaseModel):
    chapter_number: int
    title: Optional[str] = None
    pages: List[PageCreate]

class BookCreate(BaseModel):
    title: str
    author: Optional[str] = None
    summary: Optional[str] = None
    cover_url: Optional[str] = None
    genre: Optional[str] = None
    chapters: List[ChapterCreate]

# Output modeli za detaljnu knjigu
class PageOut(BaseModel):
    id: int
    page_number: int
    content: str

    class Config:
        orm_mode = True

class ChapterOut(BaseModel):
    id: int
    chapter_number: int
    title: Optional[str]
    pages: List[PageOut] = []

    class Config:
        orm_mode = True

class BookOut(BaseModel):
    id: int
    title: str
    author: Optional[str]
    summary: Optional[str]
    cover_url: Optional[str]
    genre: Optional[str]
    chapters: List[ChapterOut] = []

    class Config:
        orm_mode = True

# GET all books (osnovni pregled)
@router.get("/books", response_model=List[BookOut])
def get_books(db: Session = Depends(get_db)):
    return db.query(Book).all()

# GET pojedinačna knjiga sa svim poglavljima i stranicama
@router.get("/books/{book_id}", response_model=BookOut)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).options(
        joinedload(Book.chapters).joinedload(Chapter.pages)
    ).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

# POST create book
@router.post("/book")
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    db_book = Book(
        title=book.title,
        author=book.author,
        summary=book.summary,
        cover_url=book.cover_url,
        genre=book.genre
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)

    for chapter_data in book.chapters:
        db_chapter = Chapter(
            book_id=db_book.id,
            chapter_number=chapter_data.chapter_number,
            title=chapter_data.title
        )
        db.add(db_chapter)
        db.commit()
        db.refresh(db_chapter)

        for page_data in chapter_data.pages:
            db_page = Page(
                chapter_id=db_chapter.id,
                page_number=page_data.page_number,
                content=page_data.content,
                book_id=db_book.id
            )
            db.add(db_page)
        db.commit()

    return {"book_id": db_book.id}

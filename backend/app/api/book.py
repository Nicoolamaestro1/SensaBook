from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.book import Book, Chapter, Page
from . import sample, soundscape
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()
router.include_router(sample.router)
router.include_router(soundscape.router)

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
                content=page_data.content
            )
            db.add(db_page)
        db.commit()

    return {"book_id": db_book.id}

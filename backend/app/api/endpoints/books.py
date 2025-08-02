from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.book import BookOut
from app.services.book import get_all_books

router = APIRouter()

@router.get("/books", response_model=list[BookOut])
def list_books(db: Session = Depends(get_db)):
    return get_all_books(db)

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.services.soundscape import get_ambient_soundscape
from app.db.session import get_db
from sqlalchemy import Column, Integer, ForeignKey

router = APIRouter(prefix="/soundscape", tags=["Soundscape"])

@router.get("/book/{book_id}/chapter{chapter_number}/page/{page_number}")
def get_soundscape(book_id: int, chapter_number: int, page_number: int, db: Session = Depends(get_db)):
    """
    Endpoint for generating a context-aware soundscape for a specific book page.
    Returns: {
        "book_id": ...,
        "book_page_id": ...,
        "summary": ...,
        "detected_scenes": ...,
        "scene_keyword_counts": ...,
        "scene_keyword_positions": ...,
        "carpet_tracks": ...,
        "triggered_sounds": ...
    }
    """
    result = get_ambient_soundscape(book_id, chapter_number, page_number, db)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

chapter_id = Column(Integer, ForeignKey("chapter.id"))
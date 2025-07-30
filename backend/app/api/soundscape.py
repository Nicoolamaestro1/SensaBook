from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.services.soundscape import get_ambient_soundscape
from app.db.session import get_db

router = APIRouter(prefix="/soundscape", tags=["Soundscape"])

@router.get("/book/{book_id}/page/{book_page_id}")
def get_soundscape(book_id: int, book_page_id: int, db: Session = Depends(get_db)):
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
    result = get_ambient_soundscape(book_id, book_page_id, db)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result
"""
Simple Soundscape API Endpoint
Clean, simple endpoint that uses the new config-driven soundscape system
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict
from ..db.session import get_db
from ..services.simple_smart_soundscape import simple_smart_soundscape_service

router = APIRouter()

@router.get("/soundscape/book/{book_id}/chapter/{chapter_number}/page/{page_number}")
async def get_soundscape(
    book_id: int,
    chapter_number: int,
    page_number: int,
    db: Session = Depends(get_db)
) -> Dict:
    """
    Get intelligent soundscape for a specific book page.
    
    This endpoint solves the Dracula problem by understanding scene context:
    - Dialogue scenes always get conversation audio (regardless of location mentions)
    - Action scenes always get action audio
    - Only descriptive scenes consider location-specific audio
    - Genre-aware adjustments are automatically applied
    
    Returns:
        Dict containing primary_audio, secondary_audio, scene analysis, and reasoning
    """
    try:
        soundscape = simple_smart_soundscape_service.get_soundscape_for_page(
            book_id=book_id,
            chapter_number=chapter_number,
            page_number=page_number,
            db=db
        )
        
        if "error" in soundscape:
            raise HTTPException(status_code=404, detail=soundscape["error"])
        
        return {
            "success": True,
            "soundscape": soundscape,
            "message": "Smart soundscape generated successfully"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate soundscape: {str(e)}")

@router.post("/soundscape/analyze")
async def analyze_text(text: str, genre: str = None) -> Dict:
    """
    Analyze text and return scene classification with audio recommendations.
    Useful for testing and debugging the scene classification system.
    
    Args:
        text: The text to analyze
        genre: Optional genre for genre-aware adjustments
    
    Returns:
        Dict containing scene analysis and audio recommendations
    """
    try:
        analysis = simple_smart_soundscape_service.analyze_text_scene(text, genre)
        
        return {
            "success": True,
            "analysis": analysis,
            "message": "Text analysis completed successfully"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to analyze text: {str(e)}")


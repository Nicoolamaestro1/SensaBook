"""
Smart Soundscape API Endpoints
Provides intelligent, scene-aware soundscape generation
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Optional
from app.db.session import get_db
from app.services.smart_soundscape import smart_soundscape_service

router = APIRouter()

@router.post("/analyze-scene")
async def analyze_scene(text: str) -> Dict:
    """
    Analyze text and classify the scene for soundscape generation.
    This solves the Dracula problem by understanding scene context.
    """
    try:
        if not text or not text.strip():
            raise HTTPException(status_code=400, detail="Text content is required")
        
        # Analyze the scene
        analysis = smart_soundscape_service.analyze_text_scene(text)
        
        return {
            "success": True,
            "analysis": analysis,
            "message": "Scene analyzed successfully"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to analyze scene: {str(e)}")

@router.post("/generate-smart-soundscape")
async def generate_smart_soundscape(
    text: str,
    book_id: Optional[int] = None,
    chapter_number: Optional[int] = None,
    page_number: Optional[int] = None
) -> Dict:
    """
    Generate intelligent soundscape based on scene classification.
    """
    try:
        if not text or not text.strip():
            raise HTTPException(status_code=400, detail="Text content is required")
        
        # Generate smart soundscape
        soundscape = smart_soundscape_service.generate_smart_soundscape(
            text=text,
            book_id=book_id,
            chapter_number=chapter_number,
            page_number=page_number
        )
        
        return {
            "success": True,
            "soundscape": soundscape,
            "message": "Smart soundscape generated successfully"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate soundscape: {str(e)}")

@router.get("/soundscape/{book_id}/{chapter_number}/{page_number}")
async def get_page_soundscape(
    book_id: int,
    chapter_number: int,
    page_number: int,
    db: Session = Depends(get_db)
) -> Dict:
    """
    Get intelligent soundscape for a specific book page.
    """
    try:
        # Get soundscape for the page
        soundscape = smart_soundscape_service.get_soundscape_for_page(
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
            "message": "Page soundscape retrieved successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get page soundscape: {str(e)}")

@router.get("/test-dracula-problem")
async def test_dracula_problem() -> Dict:
    """
    Test endpoint to demonstrate solving the Dracula hotel dinner vs castle problem.
    """
    try:
        # Test 1: Hotel dining with castle mentioned (should be hotel audio)
        hotel_text = "They sat in the hotel dining room, enjoying their meal. The castle is mentioned."
        hotel_analysis = smart_soundscape_service.analyze_text_scene(hotel_text)
        
        # Test 2: Pure castle description (should be castle audio)
        castle_text = "The castle loomed majestically over the valley."
        castle_analysis = smart_soundscape_service.analyze_text_scene(castle_text)
        
        # Test 3: Dialogue about castle (should be conversation audio)
        dialogue_text = '"The castle is impressive," he said. "Yes, very beautiful," she replied.'
        dialogue_analysis = smart_soundscape_service.analyze_text_scene(dialogue_text)
        
        return {
            "success": True,
            "message": "Dracula problem test completed",
            "tests": {
                "hotel_dining_with_castle": {
                    "text": hotel_text,
                    "analysis": hotel_analysis
                },
                "pure_castle_description": {
                    "text": castle_text,
                    "analysis": castle_analysis
                },
                "dialogue_about_castle": {
                    "text": dialogue_text,
                    "analysis": dialogue_analysis
                }
            },
            "problem_solved": (
                hotel_analysis["audio_recommendations"]["primary"] != "ambience/tense_drones.mp3" and
                castle_analysis["audio_recommendations"]["primary"] == "ambience/tense_drones.mp3" and
                dialogue_analysis["audio_recommendations"]["primary"] == "ambience/cabin.mp3"
            )
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to test Dracula problem: {str(e)}")

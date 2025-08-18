from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import List, Dict, Optional, Any
from datetime import datetime

from app.db.session import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.book import Book, Chapter, Page
from app.services.reading_analytics import reading_analytics
from app.services.simple_smart_soundscape import simple_smart_soundscape_service
from pydantic import BaseModel

router = APIRouter()
security = HTTPBearer()

# Pydantic models for responses
class SceneAnalysisResponse(BaseModel):
    primary_scene: str
    scene_context: str
    mood: str
    intensity: float
    confidence: float
    audio_priority: str
    reasoning: str
    genre_adjustments: str

class SoundscapeResponse(BaseModel):
    primary_audio: str
    secondary_audio: str
    scene_type: str
    scene_context: str
    mood: str
    intensity: float
    confidence: float
    reasoning: str
    audio_priority: str
    genre: Optional[str]
    genre_adjustments: str

class ReadingStatsResponse(BaseModel):
    total_books_read: int
    total_pages_read: int
    total_reading_time_minutes: int
    average_reading_speed_wpm: float
    current_streak_days: int
    longest_streak_days: int
    favorite_genres: List[str]
    preferred_reading_times: List[str]

class BookRecommendationResponse(BaseModel):
    book_id: int
    title: str
    author: str
    genre: str
    confidence_score: float
    reason: str

class ReadingPatternsResponse(BaseModel):
    peak_reading_times: List[str]
    preferred_session_length: Dict
    reading_speed_trends: Dict
    genre_preferences: Dict
    consistency_score: float

@router.post("/analyze-scene", response_model=SceneAnalysisResponse)
def analyze_text_scene(
    text: str,
    genre: Optional[str] = None,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Analyze the scene content of text using our simple classifier."""
    try:
        analysis = simple_smart_soundscape_service.analyze_text_scene(text, genre)
        
        return SceneAnalysisResponse(
            primary_scene=analysis["scene_analysis"]["primary_scene"],
            scene_context=analysis["scene_analysis"]["scene_context"],
            mood=analysis["scene_analysis"]["mood"],
            intensity=analysis["scene_analysis"]["intensity"],
            confidence=analysis["scene_analysis"]["confidence"],
            audio_priority=analysis["scene_analysis"]["audio_priority"],
            reasoning=analysis["scene_analysis"]["reasoning"],
            genre_adjustments=analysis["scene_analysis"]["genre_adjustments"]
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error analyzing scene: {str(e)}"
        )

@router.post("/generate-soundscape", response_model=SoundscapeResponse)
def generate_soundscape(
    text: str,
    genre: Optional[str] = None,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Generate soundscape for text using our simple system."""
    try:
        soundscape = simple_smart_soundscape_service.generate_smart_soundscape(
            text=text,
            genre=genre
        )
        
        return SoundscapeResponse(
            primary_audio=soundscape["primary_audio"],
            secondary_audio=soundscape["secondary_audio"],
            scene_type=soundscape["scene_type"],
            scene_context=soundscape["scene_context"],
            mood=soundscape["mood"],
            intensity=soundscape["intensity"],
            confidence=soundscape["confidence"],
            reasoning=soundscape["reasoning"],
            audio_priority=soundscape["audio_priority"],
            genre=soundscape["genre"],
            genre_adjustments=soundscape["genre_adjustments"]
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating soundscape: {str(e)}"
        )

@router.get("/reading-stats", response_model=ReadingStatsResponse)
def get_reading_stats(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Get reading statistics for the current user."""
    try:
        current_user = get_current_user(credentials.credentials, db)
        stats = reading_analytics.get_user_reading_stats(current_user.id, db)
        
        return ReadingStatsResponse(
            total_books_read=stats.get("total_books_read", 0),
            total_pages_read=stats.get("total_pages_read", 0),
            total_reading_time_minutes=stats.get("total_reading_time_minutes", 0),
            average_reading_speed_wpm=stats.get("average_reading_speed_wpm", 0.0),
            current_streak_days=stats.get("current_streak_days", 0),
            longest_streak_days=stats.get("longest_streak_days", 0),
            favorite_genres=stats.get("favorite_genres", []),
            preferred_reading_times=stats.get("preferred_reading_times", [])
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting reading stats: {str(e)}"
        )

@router.get("/book-recommendations", response_model=List[BookRecommendationResponse])
def get_book_recommendations(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Get book recommendations based on user preferences."""
    try:
        current_user = get_current_user(credentials.credentials, db)
        recommendations = reading_analytics.get_book_recommendations(current_user.id, db)
        
        return [
            BookRecommendationResponse(
                book_id=rec["book_id"],
                title=rec["title"],
                author=rec["author"],
                genre=rec["genre"],
                confidence_score=rec["confidence_score"],
                reason=rec["reason"]
            )
            for rec in recommendations
        ]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting recommendations: {str(e)}"
        )

@router.get("/reading-patterns", response_model=ReadingPatternsResponse)
def get_reading_patterns(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Get reading patterns and trends for the current user."""
    try:
        current_user = get_current_user(credentials.credentials, db)
        patterns = reading_analytics.get_reading_patterns(current_user.id, db)
        
        return ReadingPatternsResponse(
            peak_reading_times=patterns.get("peak_reading_times", []),
            preferred_session_length=patterns.get("preferred_session_length", {}),
            reading_speed_trends=patterns.get("reading_speed_trends", {}),
            genre_preferences=patterns.get("genre_preferences", {}),
            consistency_score=patterns.get("consistency_score", 0.0)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting reading patterns: {str(e)}"
        ) 
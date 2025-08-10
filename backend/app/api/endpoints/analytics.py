from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import List, Dict, Optional, Any
from datetime import datetime

from app.db.session import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.book import Book, Chapter, Page
from app.services.emotion_analysis import emotion_analyzer
from app.services.reading_analytics import reading_analytics
from app.services.soundscape import get_ambient_soundscape
from pydantic import BaseModel

router = APIRouter()
security = HTTPBearer()

# Pydantic models for responses
class EmotionAnalysisResponse(BaseModel):
    primary_emotion: str
    emotion_scores: Dict[str, float]
    intensity: float
    confidence: float
    keywords: List[str]
    context: str

class ThemeAnalysisResponse(BaseModel):
    primary_theme: str
    theme_scores: Dict[str, float]
    sub_themes: List[str]
    setting_elements: List[str]
    atmosphere: str

class ReadingStatsResponse(BaseModel):
    total_books_read: int
    total_pages_read: int
    total_reading_time_minutes: int
    average_reading_speed_wpm: float
    current_streak_days: int
    longest_streak_days: int
    favorite_genres: List[str]
    preferred_reading_times: List[str]
    emotional_engagement_average: float

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
    emotional_engagement_trends: Dict
    consistency_score: float

@router.post("/analyze-emotion", response_model=EmotionAnalysisResponse)
def analyze_text_emotion(
    text: str,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Analyze the emotional content of text."""
    try:
        emotion_result = emotion_analyzer.analyze_emotion(text)
        
        return EmotionAnalysisResponse(
            primary_emotion=emotion_result.primary_emotion.value,
            emotion_scores=emotion_result.emotion_scores,
            intensity=emotion_result.intensity,
            confidence=emotion_result.confidence,
            keywords=emotion_result.keywords,
            context=emotion_result.context
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error analyzing emotion: {str(e)}"
        )

@router.post("/analyze-theme", response_model=ThemeAnalysisResponse)
def analyze_text_theme(
    text: str,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Analyze the thematic content of text."""
    try:
        theme_result = emotion_analyzer.analyze_theme(text)
        
        return ThemeAnalysisResponse(
            primary_theme=theme_result.primary_theme.value,
            theme_scores=theme_result.theme_scores,
            sub_themes=theme_result.sub_themes,
            setting_elements=theme_result.setting_elements,
            atmosphere=theme_result.atmosphere
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error analyzing theme: {str(e)}"
        )

@router.get("/me/stats", response_model=ReadingStatsResponse)
def get_user_reading_stats(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Get reading statistics for the current user."""
    try:
        current_user = get_current_user(credentials, db)
        stats = reading_analytics.get_user_reading_stats(current_user.id, db)
        
        return ReadingStatsResponse(
            total_books_read=stats.get("total_books_read", 0),
            total_pages_read=stats.get("total_pages_read", 0),
            total_reading_time_minutes=stats.get("total_reading_time_minutes", 0),
            average_reading_speed_wpm=stats.get("average_reading_speed_wpm", 0.0),
            current_streak_days=stats.get("current_streak_days", 0),
            longest_streak_days=stats.get("longest_streak_days", 0),
            favorite_genres=stats.get("favorite_genres", []),
            preferred_reading_times=stats.get("preferred_reading_times", []),
            emotional_engagement_average=stats.get("emotional_engagement_average", 0.0)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting reading stats: {str(e)}"
        )

@router.get("/me/recommendations", response_model=List[BookRecommendationResponse])
def get_book_recommendations(
    limit: int = 10,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Get book recommendations for the current user."""
    try:
        current_user = get_current_user(credentials, db)
        recommendations = reading_analytics.get_book_recommendations(current_user.id, limit, db)
        
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

@router.get("/me/patterns", response_model=ReadingPatternsResponse)
def get_reading_patterns(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Get reading patterns for the current user."""
    try:
        current_user = get_current_user(credentials, db)
        patterns = reading_analytics.get_reading_patterns(current_user.id, db)
        
        return ReadingPatternsResponse(
            peak_reading_times=patterns.get("peak_reading_times", []),
            preferred_session_length=patterns.get("preferred_session_length", {}),
            reading_speed_trends=patterns.get("reading_speed_trends", {}),
            genre_preferences=patterns.get("genre_preferences", {}),
            emotional_engagement_trends=patterns.get("emotional_engagement_trends", {}),
            consistency_score=patterns.get("consistency_score", 0.0)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting reading patterns: {str(e)}"
        )

@router.post("/track-session")
def track_reading_session(
    book_id: int,
    start_time: datetime,
    end_time: datetime,
    pages_read: int,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Track a reading session for analytics."""
    try:
        current_user = get_current_user(credentials, db)
        session_data = reading_analytics.track_reading_session(
            user_id=current_user.id,
            book_id=book_id,
            start_time=start_time,
            end_time=end_time,
            pages_read=pages_read,
            db=db
        )
        
        return {"message": "Session tracked successfully", "session_id": session_data.get("session_id")}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error tracking session: {str(e)}"
        )

@router.get("/trigger-words")
def get_trigger_words() -> Dict[str, Any]:
    """Get available trigger words for sound effects."""
    try:
        # Get trigger words from emotion analysis service
        sample_text = "The sword clashed against armor as thunder roared overhead."
        trigger_words = emotion_analyzer.find_trigger_words(sample_text)
        
        return {
            "available_trigger_words": [
                "sword", "armor", "thunder", "footsteps", "door", "fire", "water", "wind",
                "magic", "battle", "forest", "castle", "mountain", "river", "storm"
            ],
            "sample_analysis": trigger_words,
            "total_available": len(trigger_words)
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting trigger words: {str(e)}"
        ) 
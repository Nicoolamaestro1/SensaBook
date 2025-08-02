from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import List, Dict, Optional
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

class SoundscapeRecommendationResponse(BaseModel):
    primary_soundscape: str
    secondary_soundscape: str
    intensity: float
    atmosphere: str
    recommended_volume: float
    sound_effects: List[str]

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

@router.post("/generate-soundscape", response_model=SoundscapeRecommendationResponse)
def generate_soundscape_recommendations(
    text: str,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Generate soundscape recommendations based on text analysis."""
    try:
        emotion_result = emotion_analyzer.analyze_emotion(text)
        theme_result = emotion_analyzer.analyze_theme(text)
        
        recommendations = emotion_analyzer.generate_soundscape_recommendations(
            emotion_result, theme_result
        )
        
        return SoundscapeRecommendationResponse(**recommendations)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating soundscape: {str(e)}"
        )

@router.get("/book/{book_id}/page/{chapter_number}/{page_number}/soundscape")
def get_book_page_soundscape(
    book_id: int,
    chapter_number: int,
    page_number: int,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Get soundscape for a specific book page."""
    try:
        soundscape = get_ambient_soundscape(book_id, chapter_number, page_number, db)
        return soundscape
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting soundscape: {str(e)}"
        )

@router.get("/me/stats", response_model=ReadingStatsResponse)
def get_user_reading_stats(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Get comprehensive reading statistics for the current user."""
    try:
        current_user = get_current_user(credentials.credentials, db)
        stats = reading_analytics.get_user_reading_stats(current_user.id, db)
        
        return ReadingStatsResponse(
            total_books_read=stats.total_books_read,
            total_pages_read=stats.total_pages_read,
            total_reading_time_minutes=stats.total_reading_time_minutes,
            average_reading_speed_wpm=stats.average_reading_speed_wpm,
            current_streak_days=stats.current_streak_days,
            longest_streak_days=stats.longest_streak_days,
            favorite_genres=stats.favorite_genres,
            preferred_reading_times=stats.preferred_reading_times,
            emotional_engagement_average=stats.emotional_engagement_average
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
    """Get personalized book recommendations for the current user."""
    try:
        current_user = get_current_user(credentials.credentials, db)
        recommendations = reading_analytics.generate_book_recommendations(
            current_user.id, limit, db
        )
        
        return [
            BookRecommendationResponse(
                book_id=rec.book_id,
                title=rec.title,
                author=rec.author,
                genre=rec.genre,
                confidence_score=rec.confidence_score,
                reason=rec.reason
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
    """Analyze user's reading patterns and provide insights."""
    try:
        current_user = get_current_user(credentials.credentials, db)
        patterns = reading_analytics.analyze_reading_patterns(current_user.id, db)
        
        return ReadingPatternsResponse(**patterns)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error analyzing patterns: {str(e)}"
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
        current_user = get_current_user(credentials.credentials, db)
        session = reading_analytics.track_reading_session(
            current_user.id, book_id, start_time, end_time, pages_read, db
        )
        
        return {
            "session_id": f"session_{current_user.id}_{book_id}_{int(start_time.timestamp())}",
            "reading_speed_wpm": session.reading_speed_wpm,
            "session_type": session.session_type.value,
            "emotional_engagement": session.emotional_engagement
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error tracking session: {str(e)}"
        )

@router.get("/books/{book_id}/emotion-analysis")
def get_book_emotion_analysis(
    book_id: int,
    chapter_number: Optional[int] = None,
    page_number: Optional[int] = None,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Get emotion analysis for a book, chapter, or specific page."""
    try:
        if chapter_number is not None and page_number is not None:
            # Analyze specific page
            page = db.query(Page).filter(
                Page.book_id == book_id,
                Page.chapter_id == chapter_number,
                Page.page_number == page_number
            ).first()
            
            if not page:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Page not found"
                )
            
            text = page.content
        elif chapter_number is not None:
            # Analyze entire chapter
            pages = db.query(Page).filter(
                Page.book_id == book_id,
                Page.chapter_id == chapter_number
            ).all()
            
            if not pages:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Chapter not found"
                )
            
            text = " ".join([page.content for page in pages])
        else:
            # Analyze entire book
            pages = db.query(Page).filter(Page.book_id == book_id).all()
            
            if not pages:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Book not found"
                )
            
            text = " ".join([page.content for page in pages])
        
        # Analyze emotion and theme
        emotion_result = emotion_analyzer.analyze_emotion(text)
        theme_result = emotion_analyzer.analyze_theme(text)
        
        return {
            "book_id": book_id,
            "chapter_number": chapter_number,
            "page_number": page_number,
            "emotion_analysis": {
                "primary_emotion": emotion_result.primary_emotion.value,
                "intensity": emotion_result.intensity,
                "confidence": emotion_result.confidence,
                "keywords": emotion_result.keywords
            },
            "theme_analysis": {
                "primary_theme": theme_result.primary_theme.value,
                "atmosphere": theme_result.atmosphere,
                "setting_elements": theme_result.setting_elements
            },
            "soundscape_recommendations": emotion_analyzer.generate_soundscape_recommendations(
                emotion_result, theme_result
            )
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error analyzing book: {str(e)}"
        ) 
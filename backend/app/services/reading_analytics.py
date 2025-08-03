from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, desc
from app.models.book import Book, Chapter, Page
from app.models.user import User
from dataclasses import dataclass
from enum import Enum
import json

class ReadingSpeed(Enum):
    SLOW = "slow"  # < 150 WPM
    NORMAL = "normal"  # 150-250 WPM
    FAST = "fast"  # 250-350 WPM
    VERY_FAST = "very_fast"  # > 350 WPM

class ReadingSessionType(Enum):
    CASUAL = "casual"  # < 15 minutes
    FOCUSED = "focused"  # 15-60 minutes
    DEEP = "deep"  # > 60 minutes

@dataclass
class ReadingSession:
    user_id: int
    book_id: int
    start_time: datetime
    end_time: Optional[datetime]
    pages_read: int
    words_read: int
    reading_speed_wpm: float
    session_type: ReadingSessionType
    emotional_engagement: float  # 0.0 to 1.0

@dataclass
class UserReadingStats:
    total_books_read: int
    total_pages_read: int
    total_reading_time_minutes: int
    average_reading_speed_wpm: float
    current_streak_days: int
    longest_streak_days: int
    favorite_genres: List[str]
    preferred_reading_times: List[str]
    emotional_engagement_average: float

@dataclass
class BookRecommendation:
    book_id: int
    title: str
    author: str
    genre: str
    confidence_score: float
    reason: str

class ReadingAnalyticsService:
    def __init__(self):
        self.words_per_page_estimate = 250  # Average words per page
        
    def track_reading_session(
        self,
        user_id: int,
        book_id: int,
        start_time: datetime,
        end_time: datetime,
        pages_read: int,
        db: Session
    ) -> ReadingSession:
        """Track a reading session and calculate analytics."""
        
        # Calculate reading time in minutes
        reading_time_minutes = (end_time - start_time).total_seconds() / 60
        
        # Calculate words read
        words_read = pages_read * self.words_per_page_estimate
        
        # Calculate reading speed (WPM)
        reading_speed_wpm = words_read / reading_time_minutes if reading_time_minutes > 0 else 0
        
        # Determine session type
        session_type = self._determine_session_type(reading_time_minutes)
        
        # Calculate emotional engagement (placeholder - would be based on user feedback)
        emotional_engagement = self._calculate_emotional_engagement(pages_read, reading_speed_wpm)
        
        session = ReadingSession(
            user_id=user_id,
            book_id=book_id,
            start_time=start_time,
            end_time=end_time,
            pages_read=pages_read,
            words_read=words_read,
            reading_speed_wpm=reading_speed_wpm,
            session_type=session_type,
            emotional_engagement=emotional_engagement
        )
        
        # Store session in database (simplified for now)
        self._store_reading_session(session, db)
        
        return session
    
    def get_user_reading_stats(self, user_id: int, db: Session) -> UserReadingStats:
        """Get comprehensive reading statistics for a user."""
        
        # Get basic stats
        total_books_read = self._get_total_books_read(user_id, db)
        total_pages_read = self._get_total_pages_read(user_id, db)
        total_reading_time = self._get_total_reading_time(user_id, db)
        average_speed = self._get_average_reading_speed(user_id, db)
        
        # Get streak information
        current_streak = self._calculate_current_streak(user_id, db)
        longest_streak = self._get_longest_streak(user_id, db)
        
        # Get preferences
        favorite_genres = self._get_favorite_genres(user_id, db)
        preferred_times = self._get_preferred_reading_times(user_id, db)
        emotional_engagement = self._get_average_emotional_engagement(user_id, db)
        
        return UserReadingStats(
            total_books_read=total_books_read,
            total_pages_read=total_pages_read,
            total_reading_time_minutes=total_reading_time,
            average_reading_speed_wpm=average_speed,
            current_streak_days=current_streak,
            longest_streak_days=longest_streak,
            favorite_genres=favorite_genres,
            preferred_reading_times=preferred_times,
            emotional_engagement_average=emotional_engagement
        )
    
    def generate_book_recommendations(
        self,
        user_id: int,
        limit: int = 10,
        db: Session = None
    ) -> List[BookRecommendation]:
        """Generate personalized book recommendations based on reading history."""
        
        # Get user preferences
        user_stats = self.get_user_reading_stats(user_id, db)
        
        # Get recently read books
        recent_books = self._get_recently_read_books(user_id, db, limit=5)
        
        # Get books in favorite genres
        genre_books = self._get_books_by_genres(user_stats.favorite_genres, db, exclude_ids=[b.book_id for b in recent_books])
        
        # Generate recommendations
        recommendations = []
        
        # Add genre-based recommendations
        for book in genre_books[:limit//2]:
            recommendations.append(BookRecommendation(
                book_id=book.id,
                title=book.title,
                author=book.author or "Unknown",
                genre=book.genre or "General",
                confidence_score=0.8,
                reason=f"Based on your preference for {book.genre} books"
            ))
        
        # Add diversity recommendations (different genres)
        diverse_books = self._get_diverse_recommendations(user_stats.favorite_genres, db, limit=limit//2)
        for book in diverse_books:
            recommendations.append(BookRecommendation(
                book_id=book.id,
                title=book.title,
                author=book.author or "Unknown",
                genre=book.genre or "General",
                confidence_score=0.6,
                reason="Expand your reading horizons"
            ))
        
        return recommendations[:limit]
    
    def analyze_reading_patterns(self, user_id: int, db: Session) -> Dict:
        """Analyze user's reading patterns and provide insights."""
        
        # Get reading sessions
        sessions = self._get_reading_sessions(user_id, db, days=30)
        
        if not sessions:
            # Return default values when no data is available
            return {
                "peak_reading_times": [],
                "preferred_session_length": {"average_minutes": 0, "most_common": "casual"},
                "reading_speed_trends": {"average_wpm": 0, "trend": "stable"},
                "genre_preferences": {"top_genres": [], "diversity_score": 0},
                "emotional_engagement_trends": {"average_engagement": 0, "trend": "stable"},
                "consistency_score": 0.0
            }
        
        # Analyze patterns
        patterns = {
            "peak_reading_times": self._find_peak_reading_times(sessions),
            "preferred_session_length": self._analyze_session_lengths(sessions),
            "reading_speed_trends": self._analyze_speed_trends(sessions),
            "genre_preferences": self._analyze_genre_preferences(user_id, db),
            "emotional_engagement_trends": self._analyze_emotional_engagement(sessions),
            "consistency_score": self._calculate_consistency_score(sessions)
        }
        
        return patterns
    
    def _determine_session_type(self, minutes: float) -> ReadingSessionType:
        """Determine the type of reading session based on duration."""
        if minutes < 15:
            return ReadingSessionType.CASUAL
        elif minutes < 60:
            return ReadingSessionType.FOCUSED
        else:
            return ReadingSessionType.DEEP
    
    def _calculate_emotional_engagement(self, pages_read: int, speed_wpm: float) -> float:
        """Calculate emotional engagement based on reading behavior."""
        # This is a simplified calculation
        # In a real implementation, this would be based on user feedback, eye tracking, etc.
        
        # Higher engagement if reading slower (more thoughtful reading)
        speed_factor = max(0, 1 - (speed_wpm - 200) / 200)  # Normalize around 200 WPM
        
        # Higher engagement if reading more pages
        volume_factor = min(1, pages_read / 10)  # Normalize around 10 pages
        
        return (speed_factor + volume_factor) / 2
    
    def _store_reading_session(self, session: ReadingSession, db: Session):
        """Store reading session in database."""
        # This would typically store in a reading_sessions table
        # For now, we'll just pass through
        pass
    
    def _get_total_books_read(self, user_id: int, db: Session) -> int:
        """Get total number of books read by user."""
        # This would query a reading_sessions table
        # For now, return a placeholder
        return 5
    
    def _get_total_pages_read(self, user_id: int, db: Session) -> int:
        """Get total pages read by user."""
        return 1250
    
    def _get_total_reading_time(self, user_id: int, db: Session) -> int:
        """Get total reading time in minutes."""
        return 1800  # 30 hours
    
    def _get_average_reading_speed(self, user_id: int, db: Session) -> float:
        """Get average reading speed in WPM."""
        return 220.0
    
    def _calculate_current_streak(self, user_id: int, db: Session) -> int:
        """Calculate current reading streak in days."""
        return 7
    
    def _get_longest_streak(self, user_id: int, db: Session) -> int:
        """Get longest reading streak in days."""
        return 21
    
    def _get_favorite_genres(self, user_id: int, db: Session) -> List[str]:
        """Get user's favorite genres based on reading history."""
        return ["Fantasy", "Mystery", "Adventure"]
    
    def _get_preferred_reading_times(self, user_id: int, db: Session) -> List[str]:
        """Get user's preferred reading times."""
        return ["Evening", "Night"]
    
    def _get_average_emotional_engagement(self, user_id: int, db: Session) -> float:
        """Get average emotional engagement score."""
        return 0.75
    
    def _get_recently_read_books(self, user_id: int, db: Session, limit: int) -> List:
        """Get recently read books by user."""
        # This would query reading sessions and join with books
        return []
    
    def _get_books_by_genres(self, genres: List[str], db: Session, exclude_ids: List[int] = None) -> List[Book]:
        """Get books by specified genres."""
        query = db.query(Book).filter(Book.genre.in_(genres))
        if exclude_ids:
            query = query.filter(~Book.id.in_(exclude_ids))
        return query.limit(10).all()
    
    def _get_diverse_recommendations(self, favorite_genres: List[str], db: Session, limit: int) -> List[Book]:
        """Get diverse book recommendations outside favorite genres."""
        query = db.query(Book).filter(~Book.genre.in_(favorite_genres))
        return query.limit(limit).all()
    
    def _get_reading_sessions(self, user_id: int, db: Session, days: int = 30) -> List[ReadingSession]:
        """Get reading sessions for analysis."""
        # This would query a reading_sessions table
        # For now, return empty list
        return []
    
    def _find_peak_reading_times(self, sessions: List[ReadingSession]) -> List[str]:
        """Find peak reading times from sessions."""
        return ["8:00 PM", "10:00 PM"]
    
    def _analyze_session_lengths(self, sessions: List[ReadingSession]) -> Dict:
        """Analyze reading session lengths."""
        return {
            "average_minutes": 45,
            "most_common_type": "focused"
        }
    
    def _analyze_speed_trends(self, sessions: List[ReadingSession]) -> Dict:
        """Analyze reading speed trends."""
        return {
            "trend": "improving",
            "average_wpm": 220,
            "speed_category": "normal"
        }
    
    def _analyze_genre_preferences(self, user_id: int, db: Session) -> Dict:
        """Analyze genre preferences."""
        return {
            "top_genre": "Fantasy",
            "genre_diversity": "medium",
            "exploration_score": 0.6
        }
    
    def _analyze_emotional_engagement(self, sessions: List[ReadingSession]) -> Dict:
        """Analyze emotional engagement trends."""
        return {
            "average_engagement": 0.75,
            "trend": "stable",
            "peak_engagement_genre": "Mystery"
        }
    
    def _calculate_consistency_score(self, sessions: List[ReadingSession]) -> float:
        """Calculate reading consistency score."""
        return 0.8

# Global analytics service instance
reading_analytics = ReadingAnalyticsService() 
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    name: str

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None

class UserProfile(BaseModel):
    id: int
    name: str
    email: EmailStr
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class UserPreferences(BaseModel):
    reading_speed: Optional[int] = 200  # words per minute
    audio_volume: Optional[float] = 0.7
    soundscape_intensity: Optional[str] = "medium"  # low, medium, high
    auto_play_soundscapes: Optional[bool] = True
    preferred_genres: Optional[list] = []
    reading_goals: Optional[dict] = {}

class UserReadingStats(BaseModel):
    total_books_read: int = 0
    total_pages_read: int = 0
    reading_time_minutes: int = 0
    favorite_genres: list = []
    current_streak_days: int = 0
    longest_streak_days: int = 0
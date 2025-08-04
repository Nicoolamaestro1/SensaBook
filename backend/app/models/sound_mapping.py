from sqlalchemy import Column, Integer, String, Text, ForeignKey, JSON, Float, Boolean
from sqlalchemy.orm import relationship
from app.db.session import Base

class BookSoundMapping(Base):
    __tablename__ = "book_sound_mappings"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("book.id"), nullable=False)
    mapping_type = Column(String, nullable=False)  # 'scene' or 'word'
    scene_name = Column(String, nullable=True)  # For scene mappings: 'dracula_castle', 'dracula_night', etc.
    keywords = Column(JSON, nullable=False)  # Array of keywords to match
    sound_file = Column(String, nullable=False)  # The MP3 file to play
    priority = Column(Integer, default=0)  # Priority for scene mappings
    description = Column(Text, nullable=True)  # Description of the sound effect
    
    # Relationship to book
    book = relationship("Book", back_populates="sound_mappings")

# Update the Book model to include the relationship
class Book(Base):
    __tablename__ = "book"
    
    # ... existing fields ...
    sound_mappings = relationship("BookSoundMapping", back_populates="book", order_by="BookSoundMapping.priority.desc()")

class SoundFile(Base):
    __tablename__ = "sound_files"
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, unique=True, nullable=False)  # e.g., 'vampire_hiss.mp3'
    description = Column(Text, nullable=True)  # Human-readable description
    category = Column(String, nullable=True)  # 'ambient', 'effect', 'music', etc.
    duration = Column(Float, nullable=True)  # Duration in seconds
    file_size = Column(Integer, nullable=True)  # File size in bytes
    is_available = Column(Boolean, default=True)  # Whether the file exists and is ready 
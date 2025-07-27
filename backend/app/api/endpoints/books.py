from fastapi import APIRouter, HTTPException
from app.models.book import Book  # adjust import as needed
from sqlalchemy.orm import Session
from app.db.session import get_db
from fastapi import Depends

router = APIRouter()

# Dummy emotion analyzer
def analyze_emotion(text: str) -> str:
    # Replace with real NLP later
    if "sad" in text.lower():
        return "sad"
    elif "happy" in text.lower():
        return "happy"
    return "neutral"

# Dummy sound mapper
def get_sound_for_emotion(emotion: str) -> str:
    sounds = {
        "happy": "happy_song.mp3",
        "sad": "sad_violin.mp3",
        "neutral": "calm_ambient.mp3"
    }
    return sounds.get(emotion, "default_sound.mp3")

@router.get("/books/{book_id}/chapter/{chapter_num}/sound")
def get_chapter_sound(book_id: int, chapter_num: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    # Assume book.chapters is a list of chapter texts
    try:
        chapter_text = book.chapters[chapter_num - 1]
    except (IndexError, AttributeError):
        raise HTTPException(status_code=404, detail="Chapter not found")
    emotion = analyze_emotion(chapter_text)
    sound = get_sound_for_emotion(emotion)
    return {"emotion": emotion, "sound": sound}
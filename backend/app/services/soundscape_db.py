import re
from collections import Counter, defaultdict
from typing import List, Dict, Tuple
from sqlalchemy.orm import Session
from app.models.sound_mapping import BookSoundMapping
from app.models.book import get_page

def get_database_scene_detection(text: str, book_id: int, db: Session) -> Tuple[List[str], Dict[str, int], Dict[str, List[int]]]:
    """
    Returns scene detection using database mappings instead of hardcoded ones.
    """
    text = text.lower()
    scene_counter = Counter()
    scene_positions = defaultdict(list)
    
    # Get scene mappings from database for this book
    scene_mappings = db.query(BookSoundMapping).filter(
        BookSoundMapping.book_id == book_id,
        BookSoundMapping.mapping_type == 'scene'
    ).order_by(BookSoundMapping.priority.desc()).all()
    
    # Simple keyword matching using database mappings
    for mapping in scene_mappings:
        for keyword in mapping.keywords:
            if keyword in text:
                scene_counter[mapping.scene_name] += 1
                # Find position (simplified)
                pos = text.find(keyword)
                if pos != -1:
                    scene_positions[mapping.scene_name].append(pos)

    sorted_scenes = sorted(
        scene_counter,
        key=lambda s: (-scene_counter[s], s)
    )
    return sorted_scenes, dict(scene_counter), dict(scene_positions)

def get_database_triggered_sounds(text: str, book_id: int, db: Session) -> List[Dict]:
    """
    Detects individual sound words using database mappings.
    """
    text = text.lower()
    triggered = []
    
    # Get word mappings from database for this book
    word_mappings = db.query(BookSoundMapping).filter(
        BookSoundMapping.book_id == book_id,
        BookSoundMapping.mapping_type == 'word'
    ).all()
    
    for mapping in word_mappings:
        for keyword in mapping.keywords:
            if keyword in text:
                pos = text.find(keyword)
                triggered.append({
                    "word": keyword,
                    "sound": mapping.sound_file,
                    "position": pos
                })
    
    return triggered

def get_contextual_summary(text: str) -> str:
    """
    Returns the first sentence as a simple summary.
    """
    sentences = text.split('.')
    if sentences:
        return sentences[0].strip()
    return text[:120] + "..." if len(text) > 120 else text

def get_database_ambient_soundscape(book_id: int, chapter_number: int, page_number: int, db: Session) -> Dict:
    """
    Returns a structured soundscape dict using database mappings.
    """
    book_page = get_page(book_id=book_id, chapter_number=chapter_number, page_number=page_number, db=db)
    if not book_page:
        return {"error": "Book page not found"}

    text = book_page.content
    sorted_scenes, scene_counts, scene_positions = get_database_scene_detection(text, book_id, db)
    triggered_sounds = get_database_triggered_sounds(text, book_id, db)
    context_summary = get_contextual_summary(text)

    # Get carpet tracks based on detected scenes from database
    carpet_tracks = []
    for scene_name in sorted_scenes[:2]:  # Top 2 scenes
        mapping = db.query(BookSoundMapping).filter(
            BookSoundMapping.book_id == book_id,
            BookSoundMapping.mapping_type == 'scene',
            BookSoundMapping.scene_name == scene_name
        ).first()
        if mapping:
            carpet_tracks.append(mapping.sound_file)
    
    # If no scenes detected, use default tracks
    if not carpet_tracks:
        # Get default mapping for this book
        default_mapping = db.query(BookSoundMapping).filter(
            BookSoundMapping.book_id == book_id,
            BookSoundMapping.scene_name == 'default'
        ).first()
        if default_mapping:
            carpet_tracks = [default_mapping.sound_file]
        else:
            carpet_tracks = ["default_ambience.mp3"]

    return {
        "book_id": book_id,
        "chapter_id": chapter_number,
        "page_id": page_number,
        "summary": context_summary,
        "detected_scenes": sorted_scenes,
        "scene_keyword_counts": scene_counts,
        "scene_keyword_positions": scene_positions,
        "carpet_tracks": carpet_tracks,
        "triggered_sounds": triggered_sounds
    }

def create_dracula_sound_mappings(db: Session):
    """
    Helper function to create Dracula sound mappings in the database.
    This replaces the hardcoded Python mappings.
    """
    dracula_mappings = [
        # Scene mappings
        {
            "book_id": 10,
            "mapping_type": "scene",
            "scene_name": "dracula_castle",
            "keywords": ["castle", "dracula", "count", "vampire", "tomb", "grave", "coffin", "undead", "blood", "throat"],
            "sound_file": "gothic_castle_ambience.mp3",
            "priority": 5,
            "description": "Dark, echoing castle atmosphere"
        },
        {
            "book_id": 10,
            "mapping_type": "scene",
            "scene_name": "dracula_night",
            "keywords": ["night", "dark", "darkness", "shadow", "shadows", "moon", "stars", "starry", "evening", "dusk", "twilight", "black", "gloom", "obscure"],
            "sound_file": "night_ambience.mp3",
            "priority": 3,
            "description": "Quiet night sounds"
        },
        {
            "book_id": 10,
            "mapping_type": "scene",
            "scene_name": "dracula_storm",
            "keywords": ["storm", "thunder", "lightning", "clouds", "dark clouds", "tempest", "gale", "wind", "stormy", "thunderstorm", "tempestuous"],
            "sound_file": "storm_ambience.mp3",
            "priority": 4,
            "description": "Storm atmosphere"
        },
        {
            "book_id": 10,
            "mapping_type": "scene",
            "scene_name": "dracula_wolves",
            "keywords": ["wolf", "wolves", "howling", "beast", "animal", "wild", "hunt", "prey"],
            "sound_file": "wolf_howls.mp3",
            "priority": 6,
            "description": "Wolf pack howling"
        },
        
        # Word mappings
        {
            "book_id": 10,
            "mapping_type": "word",
            "keywords": ["dracula", "vampire"],
            "sound_file": "vampire_hiss.mp3",
            "priority": 1,
            "description": "Dracula's menacing hiss"
        },
        {
            "book_id": 10,
            "mapping_type": "word",
            "keywords": ["blood"],
            "sound_file": "blood_drip.mp3",
            "priority": 1,
            "description": "Dripping blood sound"
        },
        {
            "book_id": 10,
            "mapping_type": "word",
            "keywords": ["thunder"],
            "sound_file": "thunder_roll.mp3",
            "priority": 1,
            "description": "Deep thunder rumble"
        },
        {
            "book_id": 10,
            "mapping_type": "word",
            "keywords": ["wolf", "wolves"],
            "sound_file": "wolf_howl.mp3",
            "priority": 1,
            "description": "Wolf howl"
        },
        {
            "book_id": 10,
            "mapping_type": "word",
            "keywords": ["footsteps"],
            "sound_file": "footsteps_stone.mp3",
            "priority": 1,
            "description": "Footsteps on stone"
        },
        {
            "book_id": 10,
            "mapping_type": "word",
            "keywords": ["door"],
            "sound_file": "door_creak.mp3",
            "priority": 1,
            "description": "Door creaking"
        }
    ]
    
    for mapping_data in dracula_mappings:
        # Check if mapping already exists
        existing = db.query(BookSoundMapping).filter(
            BookSoundMapping.book_id == mapping_data["book_id"],
            BookSoundMapping.mapping_type == mapping_data["mapping_type"],
            BookSoundMapping.scene_name == mapping_data.get("scene_name")
        ).first()
        
        if not existing:
            db_mapping = BookSoundMapping(**mapping_data)
            db.add(db_mapping)
    
    db.commit()
    return {"message": f"Created {len(dracula_mappings)} sound mappings for Dracula"} 
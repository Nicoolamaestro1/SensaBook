import re
from collections import Counter, defaultdict
from typing import List, Dict, Tuple
from sqlalchemy.orm import Session
from .book import get_page

# Define priority for scene-based ambience layering
CARPET_PRIORITY = [
    "fear", "storm",  "indoors", "castle", "hotel",
    "library", "forest", "mountains", "travel", "eating"
]

# Main mapping of scenes to keywords and their carpet tracks
SCENE_SOUND_MAPPINGS = {
    "eating": {
        "keywords": ["dinner", "supper", "eating", "meal", "restaurant", "food", "dining", "feast"],
        "carpet": "ambience/atmosphere-sound-effect-239969.mp3"
    },
    "hotel": {
        "keywords": ["hotel", "lobby", "room service", "inn", "accommodation", "reception"],
        "carpet": "ambience/atmosphere-sound-effect-239969.mp3"
    },
    "library": {
        "keywords": ["museum", "library", "books", "research", "study", "academic", "scholarly"],
        "carpet": "ambience/default_ambience.mp3"
    },
    "travel": {
        "keywords": ["carriage", "train", "journey", "trip", "traveling", "voyage", "expedition"],
        "carpet": "ambience/footsteps-approaching-316715.mp3"
    },
    "storm": {
        "keywords": ["storm", "thunder", "lightning", "rain", "downpour", "tempest", "gale"],
        "carpet": "ambience/stormy_night.mp3"
    },
    "forest": {
        "keywords": ["forest", "trees", "woods", "grove", "thicket", "wilderness"],
        "carpet": "ambience/windy_mountains.mp3"
    },
    "castle": {
        "keywords": ["castle", "keep", "tower", "gates", "fortress", "palace", "citadel"],
        "carpet": "ambience/tense_drones.mp3"
    },
    "mountains": {
        "keywords": ["mountains", "cliff", "peak", "valley", "summit", "ridge", "alpine"],
        "carpet": "ambience/windy_mountains.mp3"
    },
    "fear": {
        "keywords": ["superstition", "afraid", "creepy", "haunted", "dark", "disaster", "evil", "terrifying"],
        "carpet": "ambience/tense_drones.mp3"
    },
    "indoors": {
        "keywords": ["cabin", "indoors", "inside", "house", "room", "building", "apartment", "home", "wall", "walls", "roof"],
        "carpet": "ambience/cabin.mp3"
    }
}

def advanced_scene_detection(text: str) -> Tuple[List[str], Dict[str, int], Dict[str, List[int]]]:
    """
    Detect scenes in text and return scene information.
    """
    if not text:
        return [], {}, {}
    
    text_lower = text.lower()
    detected_scenes = []
    scene_counts = {}
    scene_positions = {}
    
    for scene_name, scene_data in SCENE_SOUND_MAPPINGS.items():
        keywords = scene_data["keywords"]
        matches = []
        
        for keyword in keywords:
            # Find all occurrences of the keyword
            positions = [m.start() for m in re.finditer(r'\b' + re.escape(keyword) + r'\b', text_lower)]
            if positions:
                matches.extend(positions)
        
        if matches:
            detected_scenes.append(scene_name)
            scene_counts[scene_name] = len(matches)
            scene_positions[scene_name] = matches
    
    # Sort scenes by frequency (most frequent first)
    sorted_scenes = sorted(detected_scenes, key=lambda x: scene_counts[x], reverse=True)
    
    return sorted_scenes, scene_counts, scene_positions

def detect_triggered_sounds(text: str) -> List[Dict]:
    """
    Detect specific words that should trigger sound effects.
    """
    # Use the emotion analysis for trigger word detection
    from .emotion_analysis import find_trigger_words
    return find_trigger_words(text)

def get_contextual_summary(text: str) -> str:
    """Generate a contextual summary of the text for debugging."""
    if not text:
        return "Empty text"
    
    # Get scene detection
    sorted_scenes, scene_counts, scene_positions = advanced_scene_detection(text)
    
    summary_parts = []
    
    if sorted_scenes:
        scene_info = [f"{scene}({scene_counts[scene]})" for scene in sorted_scenes[:3]]
        summary_parts.append(f"Scenes: {', '.join(scene_info)}")
    
    # Add trigger word info
    trigger_words = detect_triggered_sounds(text)
    if trigger_words:
        trigger_words_list = [tw["word"] for tw in trigger_words]
        summary_parts.append(f"Triggers: {', '.join(trigger_words_list)}")
    
    return "; ".join(summary_parts) if summary_parts else "No scenes or triggers detected"

def get_ambient_soundscape(book_id: int, chapter_number: int, page_number: int, db: Session) -> Dict:
    """
    Returns a structured soundscape dict for a specific book page.
    Uses scene detection for carpet sounds and emotion analysis for trigger sounds.
    """
    from app.models.book import Book
    
    # Get the book and page
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        return {"error": "Book not found"}
    
    book_page = get_page(book_id=book_id, chapter_number=chapter_number, page_number=page_number, db=db)
    if not book_page:
        return {"error": "Book page not found"}

    # Get scene detection for carpet sounds
    sorted_scenes, scene_counts, scene_positions = advanced_scene_detection(book_page.content)
    
    # Determine carpet sound based on detected scenes
    carpet_tracks = []
    if sorted_scenes:
        # Use the most frequent scene for carpet sound
        primary_scene = sorted_scenes[0]
        if primary_scene in SCENE_SOUND_MAPPINGS:
            carpet_sound = SCENE_SOUND_MAPPINGS[primary_scene]["carpet"]
            carpet_tracks.append(carpet_sound)
    
    # Get trigger sounds using emotion analysis
    triggered_sounds = detect_triggered_sounds(book_page.content)
    
    # Generate contextual summary
    context_summary = get_contextual_summary(book_page.content)

    return {
        "book_id": book_id,
        "chapter_id": chapter_number,
        "page_id": page_number,
        "summary": context_summary,
        "detected_scenes": sorted_scenes,
        "scene_keyword_counts": scene_counts,
        "scene_keyword_positions": scene_positions,
        "carpet_tracks": carpet_tracks,
        "triggered_sounds": triggered_sounds,
        "mood": "scene_based",  # Indicate this is scene-based analysis
        "confidence": len(sorted_scenes) / 10.0,  # Simple confidence based on scene detection
        "reasoning": f"Detected scenes: {', '.join(sorted_scenes) if sorted_scenes else 'none'}"
    }

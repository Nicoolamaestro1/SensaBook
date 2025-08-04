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
        "carpet": "restaurant_murmur.mp3"
    },
    "hotel": {
        "keywords": ["hotel", "lobby", "room service", "inn", "accommodation", "reception"],
        "carpet": "hotel_lobby.mp3"
    },
    "library": {
        "keywords": ["museum", "library", "books", "research", "study", "academic", "scholarly"],
        "carpet": "quiet_museum.mp3"
    },
    "travel": {
        "keywords": ["carriage", "train", "journey", "trip", "traveling", "voyage", "expedition"],
        "carpet": "horse_carriage.mp3"
    },
    "storm": {
        "keywords": ["storm", "thunder", "lightning", "rain", "downpour", "tempest", "gale"],
        "carpet": "stormy_night.mp3"
    },
    "forest": {
        "keywords": ["forest", "trees", "woods", "grove", "thicket", "wilderness"],
        "carpet": "night_forest.mp3"
    },
    "castle": {
        "keywords": ["castle", "keep", "tower", "gates", "fortress", "palace", "citadel"],
        "carpet": "stone_echoes.mp3"
    },
    "mountains": {
        "keywords": ["mountains", "cliff", "peak", "valley", "summit", "ridge", "alpine"],
        "carpet": "windy_mountains.mp3"
    },
    "fear": {
        "keywords": ["superstition", "afraid", "creepy", "haunted", "dark", "disaster", "evil", "terrifying"],
        "carpet": "tense_drones.mp3"
    },
    "indoors": {
        "keywords": ["cabin", "indoors", "inside", "house", "room", "building", "apartment", "home", "wall", "walls",
        "roof"],
        "carpet": "cabin.mp3"
    }
}

# Specific word-level sound triggers
WORD_TO_SOUND = {
    "thunder": "thunder-city-377703.mp3",
    "lightning": "flash_pop.mp3",
    "door": "door_creak.mp3",
    "bird": "bird_chirp.mp3",
    "horse": "horse_neigh.mp3",
    "owl": "owl_hoot.mp3",
    "scream": "distant_scream.mp3",
    "fire": "fire_crackle.mp3",
    "wind": "wind.mp3",
    "chains": "chains_rattle.mp3",
    "footsteps": "footstep_wood.mp3",
    "clank": "armor_clank.mp3",
    "book": "page_turn.mp3",
    "bell": "bell_ring.mp3",
    "creak": "wood_creak.mp3",
    "laugh": "soft_laughter.mp3",
    "heartbeat": "heartbeat_slow.mp3",
    "whisper": "whisper_ghostly.mp3"
}

def advanced_scene_detection(text: str) -> Tuple[List[str], Dict[str, int], Dict[str, List[int]]]:
    """
    Returns:
        - a sorted list of detected scenes (by context relevance and priority)
        - a dict of scene:frequency
        - a dict of scene:[token positions]
    """
    text = text.lower()
    scene_counter = Counter()
    scene_positions = defaultdict(list)
    
    # Simple keyword matching
    for scene, data in SCENE_SOUND_MAPPINGS.items():
        for keyword in data["keywords"]:
            if keyword in text:
                scene_counter[scene] += 1
                # Find position (simplified)
                pos = text.find(keyword)
                if pos != -1:
                    scene_positions[scene].append(pos)

    sorted_scenes = sorted(
        scene_counter,
        key=lambda s: (-scene_counter[s], CARPET_PRIORITY.index(s) if s in CARPET_PRIORITY else 999)
    )
    return sorted_scenes, dict(scene_counter), dict(scene_positions)

def detect_triggered_sounds(text: str) -> List[Dict]:
    """
    Detects individual sound words in the text and maps them to sound effects.
    """
    text = text.lower()
    triggered = []
    
    for word, sound in WORD_TO_SOUND.items():
        if word in text:
            pos = text.find(word)
            triggered.append({
                "word": word,
                "sound": sound,
                "position": pos
            })
    
    return triggered

def get_contextual_summary(text: str) -> str:
    """
    Returns the first sentence as a simple summary.
    Can be replaced with a true summarizer later.
    """
    sentences = text.split('.')
    if sentences:
        return sentences[0].strip()
    return text[:120] + "..." if len(text) > 120 else text

def get_ambient_soundscape(book_id: int, chapter_number: int, page_number: int, db: Session) -> Dict:
    """
    Returns a structured soundscape dict for the given book page.
    Combines ambient carpet tracks and triggered sounds.
    """
    book_page = get_page(book_id=book_id, chapter_number=chapter_number, page_number=page_number, db=db)
    if not book_page:
        return {"error": "Book page not found"}

    text = book_page.content
    sorted_scenes, scene_counts, scene_positions = advanced_scene_detection(text)
    triggered_sounds = detect_triggered_sounds(text)
    context_summary = get_contextual_summary(text)

    # Get carpet tracks based on detected scenes
    carpet_tracks = [
        SCENE_SOUND_MAPPINGS[s]["carpet"]
        for s in sorted_scenes[:2]
        if s in SCENE_SOUND_MAPPINGS
    ]
    
    # If no scenes detected, use default tracks
    if not carpet_tracks:
        # Cycle through available sounds based on page number
        available_sounds = [
            "windy_mountains.mp3",
        ]

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

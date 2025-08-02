import spacy
from collections import Counter, defaultdict
from typing import List, Dict, Tuple
from sqlalchemy.orm import Session
from .book import get_page

# Scene priorities can be tuned for your needs
CARPET_PRIORITY = [
    "fear", "storm", "castle", "hotel",
    "library", "forest", "mountains", "travel", "eating"
]

SCENE_SOUND_MAPPINGS = {
    "eating": {
        "keywords": ["dinner", "supper", "eating", "meal", "restaurant"],
        "carpet": "restaurant_murmur.mp3"
    },
    "hotel": {
        "keywords": ["hotel", "lobby", "room service"],
        "carpet": "hotel_lobby.mp3"
    },
    "library": {
        "keywords": ["museum", "library", "books", "research"],
        "carpet": "quiet_museum.mp3"
    },
    "travel": {
        "keywords": ["carriage", "train", "journey", "trip", "traveling"],
        "carpet": "horse_carriage.mp3"
    },
    "storm": {
        "keywords": ["storm", "thunder", "lightning", "rain", "downpour"],
        "carpet": "stormy_night.mp3"
    },
    "forest": {
        "keywords": ["forest", "trees", "woods"],
        "carpet": "night_forest.mp3"
    },
    "castle": {
        "keywords": ["castle", "keep", "tower", "gates"],
        "carpet": "stone_echoes.mp3"
    },
    "mountains": {
        "keywords": ["mountains", "cliff", "peak", "valley"],
        "carpet": "windy_mountains.mp3"
    },
    "fear": {
        "keywords": ["superstition", "afraid", "creepy", "haunted", "dark", "disaster", "evil"],
        "carpet": "tense_drones.mp3"
    }
}

WORD_TO_SOUND = {
    "thunder": "thunder_crack.mp3",
    "lightning": "flash_pop.mp3",
    "door": "door_creak.mp3",
    "bird": "bird_chirp.mp3",
    "horse": "horse_neigh.mp3",
    "owl": "owl_hoot.mp3",
    "scream": "distant_scream.mp3",
    "fire": "fire_crackle.mp3",
    "wind": "wind_blow.mp3",
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

nlp = spacy.load("en_core_web_sm")

def advanced_scene_detection(text: str) -> Tuple[List[str], Dict[str, int], Dict[str, List[int]]]:
    """
    Returns:
        - a sorted list of detected scenes (by context relevance and priority)
        - a dict of scene:frequency
        - a dict of scene:[token positions]
    """
    doc = nlp(text)
    scene_counter = Counter()
    scene_positions = defaultdict(list)

    for token in doc:
        lemma = token.lemma_.lower()
        for scene, data in SCENE_SOUND_MAPPINGS.items():
            if lemma in data["keywords"]:
                scene_counter[scene] += 1
                scene_positions[scene].append(token.idx)

    # Sort scenes by frequency (descending), then by priority (ascending)
    sorted_scenes = sorted(
        scene_counter,
        key=lambda s: (-scene_counter[s], CARPET_PRIORITY.index(s) if s in CARPET_PRIORITY else 999)
    )
    return sorted_scenes, dict(scene_counter), dict(scene_positions)

def detect_triggered_sounds(text: str) -> List[Dict]:
    doc = nlp(text)
    triggered = []
    for token in doc:
        lemma = token.lemma_.lower()
        if lemma in WORD_TO_SOUND:
            triggered.append({
                "word": token.text,
                "sound": WORD_TO_SOUND[lemma],
                "position": token.idx
            })
    return triggered

def get_contextual_summary(text: str) -> str:
    """Returns the first sentence as a simple summary. Replace with real summarizer if needed."""
    doc = nlp(text)
    for sent in doc.sents:
        return sent.text
    return text[:120] + "..." if len(text) > 120 else text

def get_ambient_soundscape(book_id: int, chapter_number: int, page_number: int, db: Session) -> Dict:
    """
    Returns soundscape data for a given book page, 
    using context-aware prioritization for carpet sounds.
    """
    book_page = get_page(book_id=book_id, chapter_number=chapter_number, page_number=page_number, db=db)
    if not book_page:
        return {"error": "Book page not found"}

    text = book_page.content
    sorted_scenes, scene_counts, scene_positions = advanced_scene_detection(text)
    triggered_sounds = detect_triggered_sounds(text)
    context_summary = get_contextual_summary(text)

    # Select up to 2 carpet tracks, using frequency+priority sorting
    carpet_tracks = [
        SCENE_SOUND_MAPPINGS[s]["carpet"]
        for s in sorted_scenes[:2]
        if s in SCENE_SOUND_MAPPINGS
    ]
    if not carpet_tracks:
        carpet_tracks = ["default_ambience.mp3"]

    # Add more context to the response for advanced use
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
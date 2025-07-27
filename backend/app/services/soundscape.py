import spacy
from .book import get_book
from sqlalchemy.orm import Session

SCENE_KEYWORDS = {
    "eating": ["dinner", "supper", "eating", "meal", "restaurant"],
    "hotel": ["hotel", "lobby", "room service"],
    "library": ["museum", "library", "books", "research"],
    "travel": ["carriage", "train", "journey", "trip", "traveling"],
    "storm": ["storm", "thunder", "lightning", "rain", "downpour"],
    "forest": ["forest", "trees", "woods"],
    "castle": ["castle", "keep", "tower", "gates"],
    "mountains": ["mountains", "cliff", "peak", "valley"],
    "fear": ["superstition", "afraid", "creepy", "haunted", "dark"],
}

SCENE_TO_SOUND = {
    "eating": "restaurant_murmur.mp3",
    "hotel": "hotel_lobby.mp3",
    "library": "quiet_museum.mp3",
    "travel": "horse_carriage.mp3",
    "storm": "stormy_night.mp3",
    "forest": "night_forest.mp3",
    "castle": "stone_echoes.mp3",
    "mountains": "windy_mountains.mp3",
    "fear": "tense_drones.mp3",
}
nlp = spacy.load("en_core_web_sm")

def advanced_scene_detection(text: str):
    doc = nlp(text)
    scenes = set()

    for token in doc:
        for scene, keywords in SCENE_KEYWORDS.items():
            if token.lemma_.lower() in keywords:
                scenes.add(scene)

    return list(scenes)

def get_ambient_soundscape(book_id: int):
    book =  get_book(db=Session, book_id=book_id)
    if not book:
        return {"error": "Book not found"}
    scenes = advanced_scene_detection(book.content)
    ambient_tracks = [SCENE_TO_SOUND[s] for s in scenes if s in SCENE_TO_SOUND]

    return {
        "book_id": book_id,
        "detected_scenes": scenes,
        "ambient_tracks": ambient_tracks or ["default_ambience.mp3"],
    }

import random

# Dummy emotion-to-sound mapping
EMOTION_TO_SOUND = {
    "happy": "birds_chirping.mp3",
    "sad": "rain_rumble.mp3",
    "tense": "low_drones.mp3",
    "romantic": "soft_piano.mp3",
    "mysterious": "forest_whispers.mp3",
}

def get_mock_emotion():
    return random.choice(list(EMOTION_TO_SOUND.keys()))

def get_soundscape_for_book(book_id: int):
    emotion = get_mock_emotion()
    return {
        "book_id": book_id,
        "emotion": emotion,
        "sound_file": EMOTION_TO_SOUND[emotion],
    }
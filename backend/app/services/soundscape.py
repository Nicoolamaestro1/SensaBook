import torch
from transformers import pipeline

# Use a model trained for emotion classification (or sentiment if that's all you need)
# You can change 'j-hartmann/emotion-english-distilroberta-base' to another supported model
emotion_classifier = pipeline(
    "text-classification",
    model="j-hartmann/emotion-english-distilroberta-base",
    return_all_scores=True
)

EMOTION_TO_SOUND = {
    "joy": "birds_chirping.mp3",
    "sadness": "rain_rumble.mp3",
    "anger": "low_drones.mp3",
    "love": "soft_piano.mp3",
    "fear": "forest_whispers.mp3",
    "surprise": "wind_chimes.mp3",
}

def analyze_emotion(text: str):
    # Analyze emotion using the HuggingFace pipeline
    results = emotion_classifier(text)
    # results[0] is a list of dicts with 'label' and 'score'
    sorted_emotions = sorted(results[0], key=lambda x: x['score'], reverse=True)
    top_emotion = sorted_emotions[0]['label']
    return top_emotion

def get_soundscape_for_book(book_text: str, book_id: int):
    emotion = analyze_emotion(book_text)
    sound_file = EMOTION_TO_SOUND.get(emotion, "default_ambient.mp3")
    return {
        "book_id": book_id,
        "emotion": emotion,
        "sound_file": sound_file,
    }

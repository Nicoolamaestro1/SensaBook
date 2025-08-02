import re
from typing import Dict, List, Tuple, Optional
from collections import Counter, defaultdict
from dataclasses import dataclass
from enum import Enum
import json

class EmotionType(Enum):
    JOY = "joy"
    SADNESS = "sadness"
    ANGER = "anger"
    FEAR = "fear"
    SURPRISE = "surprise"
    DISGUST = "disgust"
    NEUTRAL = "neutral"

class ThemeType(Enum):
    ADVENTURE = "adventure"
    ROMANCE = "romance"
    MYSTERY = "mystery"
    HORROR = "horror"
    FANTASY = "fantasy"
    DRAMA = "drama"
    COMEDY = "comedy"
    ACTION = "action"

@dataclass
class EmotionResult:
    primary_emotion: EmotionType
    emotion_scores: Dict[str, float]
    intensity: float  # 0.0 to 1.0
    confidence: float
    keywords: List[str]
    context: str

@dataclass
class ThemeResult:
    primary_theme: ThemeType
    theme_scores: Dict[str, float]
    sub_themes: List[str]
    setting_elements: List[str]
    atmosphere: str

class AdvancedEmotionAnalyzer:
    def __init__(self):
        # Emotion keywords and their weights
        self.emotion_keywords = {
            EmotionType.JOY: {
                "happy": 0.8, "joy": 0.9, "excited": 0.7, "delighted": 0.8,
                "cheerful": 0.7, "elated": 0.9, "thrilled": 0.8, "ecstatic": 0.9,
                "smile": 0.6, "laugh": 0.7, "celebrate": 0.8, "victory": 0.7,
                "wonderful": 0.7, "amazing": 0.6, "fantastic": 0.7, "brilliant": 0.6
            },
            EmotionType.SADNESS: {
                "sad": 0.8, "depressed": 0.9, "melancholy": 0.8, "grief": 0.9,
                "sorrow": 0.8, "tears": 0.7, "mourning": 0.8, "despair": 0.9,
                "lonely": 0.7, "heartbroken": 0.9, "weep": 0.7, "sorrowful": 0.8,
                "miserable": 0.8, "hopeless": 0.9, "gloomy": 0.7, "dejected": 0.8
            },
            EmotionType.ANGER: {
                "angry": 0.8, "furious": 0.9, "rage": 0.9, "irritated": 0.6,
                "enraged": 0.9, "outraged": 0.8, "fuming": 0.8, "livid": 0.9,
                "hostile": 0.8, "aggressive": 0.7, "violent": 0.8, "wrath": 0.9,
                "furious": 0.9, "incensed": 0.8, "irate": 0.8, "mad": 0.7
            },
            EmotionType.FEAR: {
                "afraid": 0.8, "terrified": 0.9, "scared": 0.7, "horrified": 0.9,
                "panic": 0.9, "dread": 0.8, "anxious": 0.6, "nervous": 0.5,
                "frightened": 0.7, "petrified": 0.9, "alarmed": 0.7, "distressed": 0.6,
                "terrifying": 0.9, "fearful": 0.7, "apprehensive": 0.6, "worried": 0.5
            },
            EmotionType.SURPRISE: {
                "surprised": 0.7, "shocked": 0.8, "amazed": 0.7, "astonished": 0.8,
                "stunned": 0.8, "bewildered": 0.6, "startled": 0.7, "astounded": 0.8,
                "incredible": 0.6, "unexpected": 0.7, "suddenly": 0.5, "abruptly": 0.5,
                "unbelievable": 0.7, "remarkable": 0.6, "extraordinary": 0.6
            },
            EmotionType.DISGUST: {
                "disgusted": 0.8, "revolted": 0.9, "repulsed": 0.8, "sickened": 0.8,
                "nauseated": 0.8, "appalled": 0.7, "horrified": 0.8, "contempt": 0.7,
                "loathing": 0.9, "abhorrent": 0.8, "vile": 0.8, "repugnant": 0.8,
                "revolting": 0.8, "disgusting": 0.8, "nauseating": 0.8
            }
        }
        
        # Theme keywords and patterns
        self.theme_keywords = {
            ThemeType.ADVENTURE: ["quest", "journey", "explore", "discover", "treasure", "map", "expedition", "adventure", "travel"],
            ThemeType.ROMANCE: ["love", "heart", "kiss", "romance", "passion", "affection", "desire", "romantic", "beloved"],
            ThemeType.MYSTERY: ["mystery", "clue", "investigate", "detective", "secret", "puzzle", "enigma", "suspense", "mysterious"],
            ThemeType.HORROR: ["horror", "terrifying", "nightmare", "haunted", "ghost", "demonic", "evil", "scary", "frightening"],
            ThemeType.FANTASY: ["magic", "wizard", "spell", "dragon", "fantasy", "enchanted", "mythical", "magical", "sorcery"],
            ThemeType.DRAMA: ["conflict", "tension", "drama", "struggle", "betrayal", "tragedy", "dramatic", "emotional"],
            ThemeType.COMEDY: ["funny", "humor", "joke", "laugh", "comedy", "amusing", "hilarious", "comical", "witty"],
            ThemeType.ACTION: ["fight", "battle", "combat", "action", "thrilling", "intense", "explosive", "warrior", "hero"]
        }
        
        # Setting and atmosphere keywords
        self.setting_keywords = {
            "indoor": ["room", "house", "building", "chamber", "hall", "kitchen", "library", "office", "bedroom"],
            "outdoor": ["forest", "mountain", "beach", "field", "garden", "park", "street", "meadow", "valley"],
            "urban": ["city", "town", "street", "building", "alley", "market", "square", "urban", "metropolitan"],
            "rural": ["village", "farm", "countryside", "meadow", "pasture", "orchard", "rural", "rustic"],
            "night": ["night", "dark", "moonlight", "stars", "midnight", "evening", "darkness", "shadow"],
            "day": ["day", "sunlight", "morning", "afternoon", "bright", "sunny", "dawn", "noon"],
            "weather": ["rain", "storm", "wind", "snow", "fog", "mist", "thunder", "lightning", "cloudy"]
        }

    def analyze_emotion(self, text: str) -> EmotionResult:
        """Analyze the emotional content of text."""
        if not text:
            return EmotionResult(
                primary_emotion=EmotionType.NEUTRAL,
                emotion_scores={},
                intensity=0.0,
                confidence=0.0,
                keywords=[],
                context=""
            )
        
        # Normalize text
        text = text.lower()
        words = re.findall(r'\b\w+\b', text)
        
        # Calculate emotion scores
        emotion_scores = defaultdict(float)
        found_keywords = []
        
        for emotion_type, keywords in self.emotion_keywords.items():
            for keyword, weight in keywords.items():
                if keyword in text:
                    emotion_scores[emotion_type.value] += weight
                    found_keywords.append(keyword)
        
        # Determine primary emotion
        if emotion_scores:
            primary_emotion = max(emotion_scores.items(), key=lambda x: x[1])
            primary_emotion_type = EmotionType(primary_emotion[0])
            intensity = min(primary_emotion[1] / 3.0, 1.0)  # Normalize to 0-1
            confidence = min(len(found_keywords) / 10.0, 1.0)
        else:
            primary_emotion_type = EmotionType.NEUTRAL
            intensity = 0.0
            confidence = 0.0
        
        # Extract context (first sentence)
        context = text.split('.')[0] if '.' in text else text[:100]
        
        return EmotionResult(
            primary_emotion=primary_emotion_type,
            emotion_scores=dict(emotion_scores),
            intensity=intensity,
            confidence=confidence,
            keywords=found_keywords,
            context=context
        )

    def analyze_theme(self, text: str) -> ThemeResult:
        """Analyze the thematic content of text."""
        if not text:
            return ThemeResult(
                primary_theme=ThemeType.DRAMA,
                theme_scores={},
                sub_themes=[],
                setting_elements=[],
                atmosphere="neutral"
            )
        
        text = text.lower()
        theme_scores = defaultdict(float)
        setting_elements = []
        atmosphere_elements = []
        
        # Calculate theme scores
        for theme_type, keywords in self.theme_keywords.items():
            for keyword in keywords:
                if keyword in text:
                    theme_scores[theme_type.value] += 1.0
        
        # Determine primary theme
        if theme_scores:
            primary_theme = max(theme_scores.items(), key=lambda x: x[1])
            primary_theme_type = ThemeType(primary_theme[0])
        else:
            primary_theme_type = ThemeType.DRAMA
        
        # Detect setting elements
        for setting_type, keywords in self.setting_keywords.items():
            for keyword in keywords:
                if keyword in text:
                    setting_elements.append(f"{setting_type}:{keyword}")
        
        # Determine atmosphere based on emotion and setting
        atmosphere = self._determine_atmosphere(text)
        
        return ThemeResult(
            primary_theme=primary_theme_type,
            theme_scores=dict(theme_scores),
            sub_themes=list(theme_scores.keys()),
            setting_elements=setting_elements,
            atmosphere=atmosphere
        )

    def _determine_atmosphere(self, text: str) -> str:
        """Determine the overall atmosphere of the text."""
        atmosphere_indicators = {
            "dark": ["dark", "shadow", "night", "black", "gloomy", "dim", "murky"],
            "bright": ["bright", "light", "sunny", "clear", "illuminated", "radiant", "luminous"],
            "tense": ["tense", "nervous", "anxious", "worried", "stressful", "strained", "strained"],
            "peaceful": ["calm", "peaceful", "tranquil", "serene", "quiet", "gentle", "soothing"],
            "energetic": ["energetic", "lively", "vibrant", "dynamic", "active", "spirited", "enthusiastic"],
            "mysterious": ["mysterious", "enigmatic", "puzzling", "curious", "strange", "cryptic", "obscure"]
        }
        
        text = text.lower()
        atmosphere_scores = defaultdict(int)
        
        for atmosphere, keywords in atmosphere_indicators.items():
            for keyword in keywords:
                if keyword in text:
                    atmosphere_scores[atmosphere] += 1
        
        if atmosphere_scores:
            return max(atmosphere_scores.items(), key=lambda x: x[1])[0]
        return "neutral"

    def generate_soundscape_recommendations(self, emotion_result: EmotionResult, theme_result: ThemeResult) -> Dict:
        """Generate soundscape recommendations based on emotion and theme analysis."""
        recommendations = {
            "primary_soundscape": self._map_emotion_to_soundscape(emotion_result.primary_emotion),
            "secondary_soundscape": self._map_theme_to_soundscape(theme_result.primary_theme),
            "intensity": emotion_result.intensity,
            "atmosphere": theme_result.atmosphere,
            "recommended_volume": self._calculate_volume(emotion_result.intensity),
            "sound_effects": self._get_sound_effects(emotion_result, theme_result)
        }
        
        return recommendations

    def _map_emotion_to_soundscape(self, emotion: EmotionType) -> str:
        """Map emotion to appropriate soundscape."""
        emotion_soundscapes = {
            EmotionType.JOY: "bright_ambience.mp3",
            EmotionType.SADNESS: "melancholy_drones.mp3",
            EmotionType.ANGER: "tense_rhythms.mp3",
            EmotionType.FEAR: "dark_ambience.mp3",
            EmotionType.SURPRISE: "sudden_impact.mp3",
            EmotionType.DISGUST: "unsettling_tones.mp3",
            EmotionType.NEUTRAL: "default_ambience.mp3"
        }
        return emotion_soundscapes.get(emotion, "default_ambience.mp3")

    def _map_theme_to_soundscape(self, theme: ThemeType) -> str:
        """Map theme to appropriate soundscape."""
        theme_soundscapes = {
            ThemeType.ADVENTURE: "epic_journey.mp3",
            ThemeType.ROMANCE: "romantic_melody.mp3",
            ThemeType.MYSTERY: "mysterious_ambience.mp3",
            ThemeType.HORROR: "horror_ambience.mp3",
            ThemeType.FANTASY: "magical_realms.mp3",
            ThemeType.DRAMA: "dramatic_tension.mp3",
            ThemeType.COMEDY: "light_hearted.mp3",
            ThemeType.ACTION: "action_rhythms.mp3"
        }
        return theme_soundscapes.get(theme, "default_ambience.mp3")

    def _calculate_volume(self, intensity: float) -> float:
        """Calculate recommended volume based on emotion intensity."""
        base_volume = 0.5
        intensity_multiplier = 0.3
        return min(base_volume + (intensity * intensity_multiplier), 1.0)

    def _get_sound_effects(self, emotion_result: EmotionResult, theme_result: ThemeResult) -> List[str]:
        """Get recommended sound effects based on analysis."""
        effects = []
        
        # Add emotion-based effects
        if emotion_result.primary_emotion == EmotionType.FEAR:
            effects.extend(["heartbeat.mp3", "distant_scream.mp3"])
        elif emotion_result.primary_emotion == EmotionType.SURPRISE:
            effects.append("sudden_impact.mp3")
        elif emotion_result.primary_emotion == EmotionType.JOY:
            effects.append("bright_chimes.mp3")
        
        # Add theme-based effects
        if theme_result.primary_theme == ThemeType.ACTION:
            effects.extend(["sword_clash.mp3", "footsteps.mp3"])
        elif theme_result.primary_theme == ThemeType.FANTASY:
            effects.append("magic_spell.mp3")
        
        return effects

# Global analyzer instance
emotion_analyzer = AdvancedEmotionAnalyzer() 
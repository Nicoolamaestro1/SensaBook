import re
from collections import Counter
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass

@dataclass
class MoodAnalysis:
    """Result of mood analysis for a page"""
    primary_mood: str
    secondary_mood: str
    confidence: float
    detected_elements: Dict[str, int]
    suggested_sound: str
    reasoning: str

class MoodAnalyzer:
    """Analyzes text content to determine atmospheric mood and suggest appropriate sounds"""
    
    # Mood categories and their characteristics
    MOOD_CATEGORIES = {
        "peaceful": {
            "keywords": ["peace", "calm", "quiet", "gentle", "soft", "tranquil", "serene", "comfortable", "cozy", "warm"],
            "sounds": ["ambience/default_ambience", "ambience/cabin", "ambience/atmosphere-sound-effect-239969"],
            "description": "Calm, comfortable, safe atmosphere"
        },
        "tense": {
            "keywords": ["tension", "fear", "anxiety", "worry", "nervous", "cautious", "suspicious", "uneasy", "apprehensive"],
            "sounds": ["ambience/tense_drones", "ambience/footsteps-approaching-316715", "ambience/stormy_night"],
            "description": "Building tension, fear, anxiety"
        },
        "epic": {
            "keywords": ["epic", "heroic", "battle", "war", "mighty", "powerful", "grand", "magnificent", "tremendous", "overwhelming"],
            "sounds": ["ambience/storm", "ambience/thunder-city-377703", "ambience/tense_drones"],
            "description": "Large-scale, heroic, powerful events"
        },
        "mystical": {
            "keywords": ["magical", "mystical", "ethereal", "otherworldly", "enchanting", "supernatural", "divine", "sacred", "ancient", "wisdom"],
            "sounds": ["ambience/atmosphere-sound-effect-239969", "ambience/default_ambience", "ambience/cabin"],
            "description": "Magical, supernatural, mystical atmosphere"
        },
        "triumphant": {
            "keywords": ["victory", "triumph", "success", "achievement", "celebration", "joy", "hope", "light", "salvation"],
            "sounds": ["ambience/default_ambience", "ambience/cabin", "ambience/atmosphere-sound-effect-239969"],
            "description": "Victory, success, celebration, hope"
        },
        "dark": {
            "keywords": ["dark", "evil", "corruption", "shadow", "death", "decay", "rotten", "corrupt", "malicious", "sinister"],
            "sounds": ["ambience/tense_drones", "ambience/stormy_night", "ambience/footsteps-approaching-316715"],
            "description": "Dark, evil, corrupt atmosphere"
        },
        "journey": {
            "keywords": ["travel", "journey", "road", "path", "walking", "riding", "moving", "adventure", "exploration"],
            "sounds": ["ambience/windy_mountains", "ambience/cabin", "ambience/default_ambience"],
            "description": "Travel, movement, adventure"
        },
        "celebration": {
            "keywords": ["party", "celebration", "festival", "joy", "laughter", "music", "dancing", "feast", "merry"],
            "sounds": ["ambience/default_ambience", "ambience/cabin", "ambience/atmosphere-sound-effect-239969"],
            "description": "Celebration, party, festive atmosphere"
        },
        "melancholy": {
            "keywords": ["sad", "melancholy", "sorrow", "grief", "lonely", "mourning", "despair", "heartbroken", "weep"],
            "sounds": ["ambience/tense_drones", "ambience/stormy_night", "ambience/cabin"],
            "description": "Sad, sorrowful, melancholic atmosphere"
        },
        "mysterious": {
            "keywords": ["mystery", "enigmatic", "puzzling", "curious", "strange", "cryptic", "obscure", "secret", "hidden"],
            "sounds": ["ambience/atmosphere-sound-effect-239969", "ambience/tense_drones", "ambience/cabin"],
            "description": "Mysterious, puzzling, enigmatic atmosphere"
        },
        "romantic": {
            "keywords": ["love", "romance", "passion", "affection", "desire", "romantic", "beloved", "heart", "kiss"],
            "sounds": ["ambience/cabin", "ambience/default_ambience", "ambience/atmosphere-sound-effect-239969"],
            "description": "Romantic, loving, passionate atmosphere"
        },
        "dangerous": {
            "keywords": ["danger", "peril", "threat", "hazardous", "risky", "deadly", "fatal", "lethal", "treacherous"],
            "sounds": ["ambience/tense_drones", "ambience/footsteps-approaching-316715", "ambience/stormy_night"],
            "description": "Dangerous, perilous, threatening atmosphere"
        },
        "hopeful": {
            "keywords": ["hope", "optimistic", "promising", "bright", "future", "possibility", "potential", "aspiration"],
            "sounds": ["ambience/default_ambience", "ambience/cabin", "ambience/atmosphere-sound-effect-239969"],
            "description": "Hopeful, optimistic, promising atmosphere"
        },
        "desperate": {
            "keywords": ["desperate", "urgent", "critical", "emergency", "last_chance", "final", "doomed", "hopeless"],
            "sounds": ["ambience/tense_drones", "ambience/storm", "ambience/footsteps-approaching-316715"],
            "description": "Desperate, urgent, critical atmosphere"
        },
        "ceremonial": {
            "keywords": ["ceremony", "ritual", "formal", "official", "sacred", "solemn", "dignified", "reverent"],
            "sounds": ["ambience/default_ambience", "ambience/cabin", "ambience/atmosphere-sound-effect-239969"],
            "description": "Ceremonial, ritual, formal atmosphere"
        }
    }
    
    # Geographic and environmental elements
    GEOGRAPHIC_ELEMENTS = {
        "mountains": ["mountain", "peak", "cliff", "ridge", "summit", "alpine", "high", "elevation"],
        "forest": ["forest", "woods", "trees", "grove", "thicket", "wilderness", "leaves", "branch"],
        "water": ["river", "stream", "lake", "water", "flowing", "crossing", "ferry", "boat"],
        "indoors": ["inside", "room", "house", "building", "chamber", "hall", "interior"],
        "plains": ["plain", "field", "grassland", "meadow", "open", "vast", "wide"],
        "ruins": ["ruin", "ancient", "stone", "echo", "old", "crumbling", "decay"]
    }
    
    # Weather and atmospheric conditions
    WEATHER_ELEMENTS = {
        "storm": ["storm", "thunder", "lightning", "rain", "tempest", "gale", "wind", "stormy"],
        "night": ["night", "dark", "evening", "dusk", "stars", "moon", "shadow"],
        "wind": ["wind", "breeze", "gust", "blowing", "air"],
        "cold": ["cold", "snow", "ice", "frost", "chill", "freezing"],
        "warm": ["warm", "sun", "heat", "hot", "fire", "burning"]
    }
    
    # Emotional intensity indicators
    EMOTIONAL_INDICATORS = {
        "high_intensity": ["desperate", "urgent", "furious", "terrifying", "overwhelming", "violent"],
        "medium_intensity": ["tense", "worried", "anxious", "cautious", "suspicious"],
        "low_intensity": ["calm", "peaceful", "gentle", "soft", "quiet", "serene"]
    }
    
    def analyze_page_mood(self, text: str) -> MoodAnalysis:
        """
        Analyzes a page of text and determines its atmospheric mood.
        Returns a MoodAnalysis object with mood classification and sound suggestion.
        """
        text_lower = text.lower()
        
        # Step 1: Count mood category keywords
        mood_scores = {}
        for mood, data in self.MOOD_CATEGORIES.items():
            score = sum(1 for keyword in data["keywords"] if keyword in text_lower)
            mood_scores[mood] = score
        
        # Step 2: Analyze geographic and weather elements
        geographic_elements = self._analyze_geographic_elements(text_lower)
        weather_elements = self._analyze_weather_elements(text_lower)
        
        # Step 3: Determine emotional intensity
        emotional_intensity = self._analyze_emotional_intensity(text_lower)
        
        # Step 4: Determine primary and secondary moods
        primary_mood, secondary_mood = self._determine_moods(mood_scores, geographic_elements, weather_elements, emotional_intensity)
        
        # Step 5: Generate sound suggestion
        suggested_sound = self._suggest_sound(primary_mood, secondary_mood, geographic_elements, weather_elements)
        
        # Step 6: Generate reasoning
        reasoning = self._generate_reasoning(primary_mood, secondary_mood, geographic_elements, weather_elements, emotional_intensity)
        
        # Step 7: Calculate confidence
        confidence = self._calculate_confidence(mood_scores, geographic_elements, weather_elements)
        
        return MoodAnalysis(
            primary_mood=primary_mood,
            secondary_mood=secondary_mood,
            confidence=confidence,
            detected_elements={
                "mood_scores": mood_scores,
                "geographic": geographic_elements,
                "weather": weather_elements,
                "emotional_intensity": emotional_intensity
            },
            suggested_sound=suggested_sound,
            reasoning=reasoning
        )
    
    def _analyze_geographic_elements(self, text: str) -> Dict[str, int]:
        """Analyzes geographic elements in the text"""
        elements = {}
        for element_type, keywords in self.GEOGRAPHIC_ELEMENTS.items():
            count = sum(1 for keyword in keywords if keyword in text)
            if count > 0:
                elements[element_type] = count
        return elements
    
    def _analyze_weather_elements(self, text: str) -> Dict[str, int]:
        """Analyzes weather and atmospheric elements in the text"""
        elements = {}
        for weather_type, keywords in self.WEATHER_ELEMENTS.items():
            count = sum(1 for keyword in keywords if keyword in text)
            if count > 0:
                elements[weather_type] = count
        return elements
    
    def _analyze_emotional_intensity(self, text: str) -> str:
        """Determines the emotional intensity level"""
        high_score = sum(1 for keyword in self.EMOTIONAL_INDICATORS["high_intensity"] if keyword in text)
        medium_score = sum(1 for keyword in self.EMOTIONAL_INDICATORS["medium_intensity"] if keyword in text)
        low_score = sum(1 for keyword in self.EMOTIONAL_INDICATORS["low_intensity"] if keyword in text)
        
        if high_score > medium_score and high_score > low_score:
            return "high"
        elif medium_score > low_score:
            return "medium"
        else:
            return "low"
    
    def _determine_moods(self, mood_scores: Dict[str, int], geographic: Dict[str, int], weather: Dict[str, int], intensity: str) -> Tuple[str, str]:
        """Determines primary and secondary moods based on analysis"""
        # Sort moods by score
        sorted_moods = sorted(mood_scores.items(), key=lambda x: x[1], reverse=True)
        
        # Get top two moods
        primary_mood = sorted_moods[0][0] if sorted_moods and sorted_moods[0][1] > 0 else "neutral"
        secondary_mood = sorted_moods[1][0] if len(sorted_moods) > 1 and sorted_moods[1][1] > 0 else "neutral"
        
        # Adjust based on geographic and weather elements
        if "mountains" in geographic and geographic["mountains"] > 2:
            if primary_mood == "neutral":
                primary_mood = "journey"
            elif secondary_mood == "neutral":
                secondary_mood = "journey"
        
        if "storm" in weather and weather["storm"] > 1:
            if intensity == "high":
                primary_mood = "epic"
            elif primary_mood == "neutral":
                primary_mood = "tense"
        
        if "night" in weather and weather["night"] > 1:
            if primary_mood == "neutral":
                primary_mood = "dark"
            elif "mystical" in mood_scores and mood_scores["mystical"] > 0:
                primary_mood = "mystical"
        
        return primary_mood, secondary_mood
    
    def _suggest_sound(self, primary_mood: str, secondary_mood: str, geographic: Dict[str, int], weather: Dict[str, int]) -> str:
        """Suggests an appropriate sound based on the mood analysis"""
        
        # Get available sounds for the primary mood
        if primary_mood in self.MOOD_CATEGORIES:
            available_sounds = self.MOOD_CATEGORIES[primary_mood]["sounds"]
            
            # Choose based on geographic/weather context
            if "mountains" in geographic and "ambience/windy_mountains" in available_sounds:
                return "ambience/windy_mountains"
            elif "forest" in geographic and "ambience/cabin" in available_sounds:
                return "ambience/cabin"
            elif "water" in geographic and "ambience/cabin_rain" in available_sounds:
                return "ambience/cabin_rain"
            elif "storm" in weather and "ambience/storm" in available_sounds:
                return "ambience/storm"
            elif "night" in weather and "ambience/stormy_night" in available_sounds:
                return "ambience/stormy_night"
            else:
                # Return first available sound for the mood
                return available_sounds[0] if available_sounds else "ambience/default_ambience"
        
        # Fallback based on secondary mood or default
        if secondary_mood in self.MOOD_CATEGORIES and self.MOOD_CATEGORIES[secondary_mood]["sounds"]:
            return self.MOOD_CATEGORIES[secondary_mood]["sounds"][0]
        
        return "ambience/default_ambience"
    
    def _generate_reasoning(self, primary_mood: str, secondary_mood: str, geographic: Dict[str, int], weather: Dict[str, int], intensity: str) -> str:
        """Generates reasoning for the mood classification"""
        reasons = []
        
        if primary_mood != "neutral":
            reasons.append(f"Primary mood: {primary_mood} ({self.MOOD_CATEGORIES[primary_mood]['description']})")
        
        if secondary_mood != "neutral" and secondary_mood != primary_mood:
            reasons.append(f"Secondary mood: {secondary_mood}")
        
        if geographic:
            reasons.append(f"Geographic elements: {', '.join(geographic.keys())}")
        
        if weather:
            reasons.append(f"Weather elements: {', '.join(weather.keys())}")
        
        reasons.append(f"Emotional intensity: {intensity}")
        
        return "; ".join(reasons)
    
    def _calculate_confidence(self, mood_scores: Dict[str, int], geographic: Dict[str, int], weather: Dict[str, int]) -> float:
        """Calculates confidence in the mood analysis"""
        total_elements = sum(mood_scores.values()) + sum(geographic.values()) + sum(weather.values())
        
        if total_elements == 0:
            return 0.0
        
        # Higher confidence with more detected elements
        confidence = min(1.0, total_elements / 10.0)
        
        # Boost confidence if we have strong mood indicators
        max_mood_score = max(mood_scores.values()) if mood_scores else 0
        if max_mood_score >= 3:
            confidence += 0.2
        
        return min(1.0, confidence)

def analyze_book_pages(book_content: List[str]) -> List[MoodAnalysis]:
    """
    Analyzes all pages of a book and returns mood analysis for each page.
    
    Args:
        book_content: List of page content strings
    
    Returns:
        List of MoodAnalysis objects for each page
    """
    analyzer = MoodAnalyzer()
    analyses = []
    
    for i, page_content in enumerate(book_content, 1):
        analysis = analyzer.analyze_page_mood(page_content)
        analyses.append(analysis)
        print(f"Page {i}: {analysis.primary_mood} -> {analysis.suggested_sound} (confidence: {analysis.confidence:.2f})")
    
    return analyses 
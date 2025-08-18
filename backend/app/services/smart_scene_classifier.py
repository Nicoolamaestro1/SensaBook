"""
Smart Scene Classification System
Advanced context-aware scene detection with intelligent audio mapping
"""

import re
import yaml
from typing import Dict, Optional, List, Tuple
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

class SceneType(Enum):
    DIALOGUE = "dialogue"
    ACTION = "action"
    DESCRIPTIVE = "descriptive"
    EMOTIONAL = "emotional"
    TRANSITION = "transition"
    NEUTRAL = "neutral"
    SUSPENSE = "suspense"
    INTIMATE = "intimate"
    EPIC = "epic"
    MYSTERIOUS = "mysterious"

class SceneContext(Enum):
    INDOOR = "indoor"
    OUTDOOR = "outdoor"
    URBAN = "urban"
    RURAL = "rural"
    NATURAL = "natural"
    BUILT = "built"
    UNDERGROUND = "underground"
    AERIAL = "aerial"
    AQUATIC = "aquatic"
    COSMIC = "cosmic"

class EmotionalIntensity(Enum):
    SUBTLE = "subtle"
    MODERATE = "moderate"
    INTENSE = "intense"
    OVERWHELMING = "overwhelming"

@dataclass
class SmartSceneAnalysis:
    primary_scene: SceneType
    scene_context: SceneContext
    mood: str
    intensity: float
    confidence: float
    audio_priority: str
    reasoning: str
    genre_adjustments: str
    emotional_arc: str
    atmospheric_qualities: List[str]
    sound_layers: List[str]
    trigger_words: List[Dict]
    ambient_suggestions: List[str]

class SmartSceneClassifier:
    """
    Advanced scene classifier that understands context, emotional arcs, and atmospheric qualities.
    Provides intelligent audio mapping based on sophisticated scene analysis.
    """
    
    def __init__(self):
        self.config_dir = Path(__file__).parent.parent.parent / "config"
        self.scene_patterns = self._load_scene_patterns()
        self.context_patterns = self._load_context_patterns()
        self.mood_patterns = self._load_mood_patterns()
        self.genre_adjustments = self._load_genre_adjustments()
        self.atmospheric_patterns = self._load_atmospheric_patterns()
        self.emotional_arcs = self._load_emotional_arcs()
    
    def _load_scene_patterns(self) -> Dict:
        """Load sophisticated scene patterns from YAML config."""
        config_file = self.config_dir / "scene_patterns.yaml"
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)
        return config["scene_types"]
    
    def _load_context_patterns(self) -> Dict:
        """Load context patterns from YAML config."""
        config_file = self.config_dir / "scene_patterns.yaml"
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)
        return config["context_patterns"]
    
    def _load_mood_patterns(self) -> Dict:
        """Load mood patterns from YAML config."""
        config_file = self.config_dir / "scene_patterns.yaml"
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)
        return config["mood_patterns"]
    
    def _load_genre_adjustments(self) -> Dict:
        """Load genre adjustments from YAML config."""
        config_file = self.config_dir / "genre_adjustments.yaml"
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)
        return config["genre_adjustments"]
    
    def _load_atmospheric_patterns(self) -> Dict:
        """Load atmospheric quality patterns."""
        config_file = self.config_dir / "scene_patterns.yaml"
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)
        return config.get("atmospheric_patterns", {})
    
    def _load_emotional_arcs(self) -> Dict:
        """Load emotional arc patterns."""
        config_file = self.config_dir / "scene_patterns.yaml"
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)
        return config.get("emotional_arcs", {})
    
    def classify_scene(self, text: str, genre: str = None) -> SmartSceneAnalysis:
        """
        Advanced scene analysis with context understanding and emotional arc detection.
        """
        if not text or not text.strip():
            return self._create_neutral_analysis()
        
        # Step 1: Analyze scene types with sophisticated pattern matching
        scene_scores = self._analyze_scene_types_advanced(text, genre)
        
        # Step 2: Determine primary scene type
        primary_scene = self._get_primary_scene(scene_scores)
        
        # Step 3: Analyze physical context with depth
        scene_context = self._analyze_context_advanced(text)
        
        # Step 4: Analyze emotional mood and intensity
        mood, intensity = self._analyze_mood_advanced(text, scene_scores, genre)
        
        # Step 5: Detect emotional arc progression
        emotional_arc = self._detect_emotional_arc(text, scene_scores)
        
        # Step 6: Analyze atmospheric qualities
        atmospheric_qualities = self._analyze_atmospheric_qualities(text, primary_scene, genre)
        
        # Step 7: Determine intelligent audio priority
        audio_priority = self._determine_smart_audio_priority(primary_scene, text, genre, atmospheric_qualities)
        
        # Step 8: Generate sound layers and ambient suggestions
        sound_layers, ambient_suggestions = self._generate_sound_recommendations(
            primary_scene, scene_context, mood, intensity, atmospheric_qualities, genre
        )
        
        # Step 9: Detect trigger words with context
        trigger_words = self._detect_contextual_triggers(text, primary_scene, mood, genre)
        
        # Step 10: Generate comprehensive reasoning
        reasoning = self._generate_advanced_reasoning(
            primary_scene, scene_scores, text, genre, atmospheric_qualities, emotional_arc
        )
        
        # Step 11: Calculate confidence with multiple factors
        confidence = self._calculate_advanced_confidence(scene_scores, atmospheric_qualities, emotional_arc)
        
        # Step 12: Generate genre adjustment explanation
        genre_adjustments = self._explain_genre_adjustments(genre, scene_scores, atmospheric_qualities)
        
        return SmartSceneAnalysis(
            primary_scene=primary_scene,
            scene_context=scene_context,
            mood=mood,
            intensity=intensity,
            confidence=confidence,
            audio_priority=audio_priority,
            reasoning=reasoning,
            genre_adjustments=genre_adjustments,
            emotional_arc=emotional_arc,
            atmospheric_qualities=atmospheric_qualities,
            sound_layers=sound_layers,
            trigger_words=trigger_words,
            ambient_suggestions=ambient_suggestions
        )
    
    def _analyze_scene_types_advanced(self, text: str, genre: str = None) -> Dict[SceneType, float]:
        """Advanced scene type analysis with context awareness and genre intelligence."""
        scene_scores = {}
        
        for scene_name, config in self.scene_patterns.items():
            scene_type = SceneType(scene_name)
            score = 0.0
            
            # Base pattern matching
            for pattern in config["patterns"]:
                matches = re.findall(pattern, text, re.IGNORECASE)
                score += len(matches) * config["base_weight"]
            
            # Context-aware scoring
            if "context_boost" in config:
                for context, boost in config["context_boost"].items():
                    if self._context_matches(text, context):
                        score *= boost
            
            # Emotional intensity correlation
            if "emotion_correlation" in config:
                emotion_score = self._calculate_emotion_correlation(text, config["emotion_correlation"])
                score += emotion_score
            
            # Genre-specific adjustments
            if genre and genre.lower() in self.genre_adjustments:
                genre_config = self.genre_adjustments[genre.lower()]
                if scene_name in genre_config:
                    score *= genre_config[scene_name]
            
            if score > 0:
                scene_scores[scene_type] = score
        
        return scene_scores
    
    def _get_primary_scene(self, scene_scores: Dict[SceneType, float]) -> SceneType:
        """Get the primary scene type based on highest score."""
        if not scene_scores:
            return SceneType.NEUTRAL
        
        primary_scene = max(scene_scores.items(), key=lambda x: x[1])
        return primary_scene[0]
    
    def _context_matches(self, text: str, context: str) -> bool:
        """Check if text matches a specific context."""
        context_patterns = {
            "night": r"\b(night|dark|moon|stars|evening|midnight)\b",
            "day": r"\b(day|sun|morning|noon|afternoon|dawn)\b",
            "storm": r"\b(storm|thunder|lightning|rain|wind|tempest)\b",
            "calm": r"\b(calm|peaceful|quiet|serene|tranquil|gentle)\b",
            "crowded": r"\b(crowd|busy|packed|bustling|teeming|swarming)\b",
            "isolated": r"\b(alone|isolated|deserted|abandoned|solitary|remote)\b"
        }
        
        if context in context_patterns:
            return bool(re.search(context_patterns[context], text, re.IGNORECASE))
        return False
    
    def _calculate_emotion_correlation(self, text: str, emotion_patterns: Dict) -> float:
        """Calculate emotional correlation score."""
        total_score = 0.0
        
        for emotion, patterns in emotion_patterns.items():
            for pattern in patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                total_score += len(matches)
        
        return total_score
    
    def _analyze_context_advanced(self, text: str) -> SceneContext:
        """Advanced context analysis with multiple layers."""
        context_scores = {}
        
        for context_name, patterns in self.context_patterns.items():
            context_type = SceneContext(context_name)
            score = 0.0
            
            # Base pattern matching
            for pattern in patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                score += len(matches)
            
            # Spatial relationship analysis
            spatial_indicators = self._analyze_spatial_relationships(text, context_name)
            score += spatial_indicators
            
            if score > 0:
                context_scores[context_type] = score
        
        if not context_scores:
            return SceneContext.INDOOR
        
        primary_context = max(context_scores.items(), key=lambda x: x[1])
        return primary_context[0]
    
    def _analyze_spatial_relationships(self, text: str, context: str) -> float:
        """Analyze spatial relationships and positioning."""
        spatial_patterns = {
            "indoor": r"\b(inside|within|interior|enclosed|confined)\b",
            "outdoor": r"\b(outside|exterior|open|exposed|uncovered)\b",
            "underground": r"\b(below|beneath|under|subterranean|buried)\b",
            "aerial": r"\b(above|overhead|soaring|flying|elevated)\b"
        }
        
        if context in spatial_patterns:
            matches = re.findall(spatial_patterns[context], text, re.IGNORECASE)
            return len(matches) * 0.5
        
        return 0.0
    
    def _analyze_mood_advanced(self, text: str, scene_scores: Dict, genre: str = None) -> Tuple[str, float]:
        """Advanced mood analysis with intensity calculation."""
        mood_scores = {}
        
        for mood, patterns in self.mood_patterns.items():
            score = 0.0
            for pattern in patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                score += len(matches)
            
            if score > 0:
                mood_scores[mood] = score
        
        if not mood_scores:
            mood = "neutral"
        else:
            primary_mood = max(mood_scores.items(), key=lambda x: x[1])
            mood = primary_mood[0]
        
        # Calculate intensity based on multiple factors
        intensity = self._calculate_advanced_intensity(text, scene_scores, mood_scores, genre)
        
        return mood, intensity
    
    def _calculate_advanced_intensity(self, text: str, scene_scores: Dict, mood_scores: Dict, genre: str = None) -> float:
        """Calculate emotional intensity using multiple factors."""
        base_intensity = 0.5
        
        # Scene type intensity
        if SceneType.ACTION in scene_scores:
            base_intensity += 0.3
        if SceneType.EMOTIONAL in scene_scores:
            base_intensity += 0.25
        if SceneType.SUSPENSE in scene_scores:
            base_intensity += 0.2
        if SceneType.EPIC in scene_scores:
            base_intensity += 0.3
        
        # Mood intensity
        intense_moods = ["tense", "fearful", "angry", "excited", "passionate"]
        for intense_mood in intense_moods:
            if intense_mood in mood_scores:
                base_intensity += 0.15
        
        # Genre intensity
        if genre and genre.lower() in self.genre_adjustments:
            if genre.lower() == "thriller":
                base_intensity += 0.2
            elif genre.lower() == "horror":
                base_intensity += 0.3
            elif genre.lower() == "romance":
                base_intensity -= 0.1
            elif genre.lower() == "epic":
                base_intensity += 0.25
        
        # Text complexity intensity
        if len(text) > 200:
            base_intensity += 0.1
        
        # Punctuation intensity (exclamation marks, etc.)
        exclamation_count = text.count('!')
        base_intensity += min(exclamation_count * 0.05, 0.2)
        
        return min(base_intensity, 1.0)
    
    def _detect_emotional_arc(self, text: str, scene_scores: Dict) -> str:
        """Detect emotional arc progression in the text."""
        # This is a simplified version - in a real system, you'd analyze the full text
        # and track emotional progression over time
        
        if SceneType.EMOTIONAL in scene_scores and scene_scores[SceneType.EMOTIONAL] > 5:
            return "emotional_buildup"
        elif SceneType.SUSPENSE in scene_scores and scene_scores[SceneType.SUSPENSE] > 3:
            return "tension_rising"
        elif SceneType.ACTION in scene_scores and scene_scores[SceneType.ACTION] > 4:
            return "climactic_moment"
        else:
            return "steady_state"
    
    def _analyze_atmospheric_qualities(self, text: str, primary_scene: SceneType, genre: str = None) -> List[str]:
        """Analyze atmospheric qualities for enhanced audio mapping."""
        qualities = []
        
        # Time-based atmosphere
        if re.search(r"\b(night|dark|moon|stars|evening)\b", text, re.IGNORECASE):
            qualities.append("nocturnal")
        elif re.search(r"\b(day|sun|morning|dawn)\b", text, re.IGNORECASE):
            qualities.append("diurnal")
        
        # Weather atmosphere
        if re.search(r"\b(storm|thunder|lightning|rain)\b", text, re.IGNORECASE):
            qualities.append("stormy")
        elif re.search(r"\b(calm|peaceful|gentle|soft)\b", text, re.IGNORECASE):
            qualities.append("serene")
        
        # Emotional atmosphere
        if re.search(r"\b(tense|anxious|worried|fearful)\b", text, re.IGNORECASE):
            qualities.append("tense")
        elif re.search(r"\b(joyful|happy|cheerful|bright)\b", text, re.IGNORECASE):
            qualities.append("uplifting")
        
        # Genre-specific atmosphere
        if genre and genre.lower() == "horror":
            qualities.append("eerie")
        elif genre and genre.lower() == "romance":
            qualities.append("intimate")
        elif genre and genre.lower() == "epic":
            qualities.append("grandiose")
        
        return qualities
    
    def _determine_smart_audio_priority(self, primary_scene: SceneType, text: str, genre: str = None, atmospheric_qualities: List[str] = None) -> str:
        """
        Determine intelligent audio priority based on multiple factors.
        This is where we solve the Dracula problem with sophisticated logic.
        """
        scene_name = primary_scene.value
        
        # For dialogue scenes - consider emotional context
        if primary_scene == SceneType.DIALOGUE:
            if "tense" in (atmospheric_qualities or []):
                return "tense_conversation_ambient"
            elif "intimate" in (atmospheric_qualities or []):
                return "intimate_conversation_ambient"
            else:
                return "conversation_ambient"
        
        # For action scenes - consider intensity and context
        elif primary_scene == SceneType.ACTION:
            if "epic" in (atmospheric_qualities or []):
                return "epic_action_rhythms"
            elif "tense" in (atmospheric_qualities or []):
                return "tense_action_background"
            else:
                return "action_rhythms"
        
        # For emotional scenes - consider mood and intensity
        elif primary_scene == SceneType.EMOTIONAL:
            if "overwhelming" in (atmospheric_qualities or []):
                return "overwhelming_emotion_ambient"
            elif "subtle" in (atmospheric_qualities or []):
                return "subtle_emotion_ambient"
            else:
                return "emotional_ambient"
        
        # For descriptive scenes - intelligent location + atmosphere combination
        elif primary_scene == SceneType.DESCRIPTIVE:
            location_priority = self._get_intelligent_location_priority(text, genre, atmospheric_qualities)
            if location_priority:
                return location_priority
        
        # Default to scene-based audio
        return self.scene_patterns[scene_name].get("audio_base", "default_ambient")
    
    def _get_intelligent_location_priority(self, text: str, genre: str = None, atmospheric_qualities: List[str] = None) -> Optional[str]:
        """Get intelligent location-specific audio with atmospheric consideration."""
        text_lower = text.lower()
        qualities = atmospheric_qualities or []
        
        # Hotel/dining with atmosphere
        if any(word in text_lower for word in ["hotel", "dining", "restaurant"]):
            if "elegant" in qualities or "formal" in qualities:
                return "elegant_hotel_dining_ambient"
            elif "cozy" in qualities or "warm" in qualities:
                return "cozy_hotel_dining_ambient"
            else:
                return "hotel_dining_ambient"
        
        # Castle with atmosphere
        if any(word in text_lower for word in ["castle", "fortress", "palace"]):
            if "eerie" in qualities or "mysterious" in qualities:
                return "eerie_castle_atmosphere"
            elif "grandiose" in qualities or "epic" in qualities:
                return "epic_castle_atmosphere"
            else:
                return "castle_atmosphere"
        
        # Forest with atmosphere
        if any(word in text_lower for word in ["forest", "woods", "jungle"]):
            if "mysterious" in qualities or "eerie" in qualities:
                return "mysterious_forest_ambient"
            elif "peaceful" in qualities or "serene" in qualities:
                return "peaceful_forest_ambient"
            else:
                return "forest_nature"
        
        # Weather-based atmosphere
        if any(word in text_lower for word in ["storm", "thunder", "lightning"]):
            if "intense" in qualities:
                return "intense_storm_weather"
            else:
                return "storm_weather"
        
        return None
    
    def _generate_sound_recommendations(self, primary_scene: SceneType, scene_context: SceneContext, mood: str, intensity: float, atmospheric_qualities: List[str], genre: str = None) -> Tuple[List[str], List[str]]:
        """Generate intelligent sound layer and ambient recommendations."""
        sound_layers = []
        ambient_suggestions = []
        
        # Primary scene layers
        scene_name = primary_scene.value
        if scene_name in self.scene_patterns:
            base_audio = self.scene_patterns[scene_name].get("audio_base", "default_ambient")
            sound_layers.append(base_audio)
        
        # Context layers
        context_audio = self._get_context_audio(scene_context, atmospheric_qualities)
        if context_audio:
            sound_layers.append(context_audio)
        
        # Mood layers
        mood_audio = self._get_mood_audio(mood, intensity)
        if mood_audio:
            sound_layers.append(mood_audio)
        
        # Atmospheric layers
        for quality in atmospheric_qualities:
            quality_audio = self._get_atmospheric_audio(quality, genre)
            if quality_audio:
                ambient_suggestions.append(quality_audio)
        
        return sound_layers, ambient_suggestions
    
    def _get_context_audio(self, scene_context: SceneContext, atmospheric_qualities: List[str]) -> Optional[str]:
        """Get context-specific audio."""
        context_audio_map = {
            SceneContext.INDOOR: "indoor_ambient",
            SceneContext.OUTDOOR: "outdoor_ambient",
            SceneContext.UNDERGROUND: "underground_ambient",
            SceneContext.AERIAL: "aerial_ambient"
        }
        
        base_audio = context_audio_map.get(scene_context)
        if not base_audio:
            return None
        
        # Enhance with atmospheric qualities
        if "eerie" in atmospheric_qualities:
            return f"eerie_{base_audio}"
        elif "peaceful" in atmospheric_qualities:
            return f"peaceful_{base_audio}"
        
        return base_audio
    
    def _get_mood_audio(self, mood: str, intensity: float) -> Optional[str]:
        """Get mood-specific audio."""
        mood_audio_map = {
            "tense": "tense_atmosphere",
            "peaceful": "peaceful_ambient",
            "exciting": "exciting_background",
            "dark": "dark_atmosphere",
            "warm": "warm_ambient"
        }
        
        return mood_audio_map.get(mood)
    
    def _get_atmospheric_audio(self, quality: str, genre: str = None) -> Optional[str]:
        """Get atmospheric quality audio."""
        quality_audio_map = {
            "nocturnal": "night_ambient",
            "stormy": "storm_weather",
            "serene": "serene_ambient",
            "tense": "tense_atmosphere",
            "uplifting": "uplifting_ambient",
            "eerie": "eerie_ambient",
            "intimate": "intimate_ambient",
            "grandiose": "epic_ambient"
        }
        
        return quality_audio_map.get(quality)
    
    def _detect_contextual_triggers(self, text: str, primary_scene: SceneType, mood: str, genre: str = None) -> List[Dict]:
        """Detect trigger words with contextual understanding."""
        # This would integrate with the trigger words system
        # For now, return empty list - will be implemented separately
        return []
    
    def _generate_advanced_reasoning(self, primary_scene: SceneType, scene_scores: Dict, text: str, genre: str = None, atmospheric_qualities: List[str] = None, emotional_arc: str = None) -> str:
        """Generate comprehensive reasoning for the classification."""
        reasons = []
        
        # Primary scene reasoning
        reasons.append(f"Primary scene: {primary_scene.value}")
        
        # Score-based reasoning
        if scene_scores:
            top_scenes = sorted(scene_scores.items(), key=lambda x: x[1], reverse=True)[:3]
            for scene, score in top_scenes:
                reasons.append(f"{scene.value}: {score:.1f}")
        
        # Atmospheric reasoning
        if atmospheric_qualities:
            reasons.append(f"Atmosphere: {', '.join(atmospheric_qualities)}")
        
        # Emotional arc reasoning
        if emotional_arc:
            reasons.append(f"Emotional arc: {emotional_arc}")
        
        # Genre reasoning
        if genre:
            reasons.append(f"Genre: {genre} (adjusted weights applied)")
        
        # Context reasoning
        if "castle" in text.lower() and primary_scene != SceneType.DESCRIPTIVE:
            reasons.append("Castle mentioned but not primary scene - using scene-based audio")
        
        return " | ".join(reasons)
    
    def _calculate_advanced_confidence(self, scene_scores: Dict, atmospheric_qualities: List[str], emotional_arc: str) -> float:
        """Calculate confidence using multiple factors."""
        base_confidence = max(scene_scores.values()) if scene_scores else 0.0
        
        # Boost confidence for atmospheric qualities
        if atmospheric_qualities:
            base_confidence += len(atmospheric_qualities) * 0.1
        
        # Boost confidence for emotional arc detection
        if emotional_arc and emotional_arc != "steady_state":
            base_confidence += 0.2
        
        return min(base_confidence, 1.0)
    
    def _explain_genre_adjustments(self, genre: str, scene_scores: Dict, atmospheric_qualities: List[str]) -> str:
        """Explain how genre affected the scene classification."""
        if not genre or genre.lower() not in self.genre_adjustments:
            return "No genre adjustments applied"
        
        genre_config = self.genre_adjustments[genre.lower()]
        adjustments = []
        
        for scene_type, score in scene_scores.items():
            if scene_type.value in genre_config:
                multiplier = genre_config[scene_type.value]
                if multiplier != 1.0:
                    adjustments.append(f"{scene_type.value}: {multiplier}x")
        
        if adjustments:
            return f"Genre '{genre}' adjustments: {', '.join(adjustments)}"
        else:
            return f"Genre '{genre}' detected but no weight adjustments needed"
    
    def _create_neutral_analysis(self) -> SmartSceneAnalysis:
        """Create a neutral analysis for empty text."""
        return SmartSceneAnalysis(
            primary_scene=SceneType.NEUTRAL,
            scene_context=SceneContext.INDOOR,
            mood="neutral",
            intensity=0.0,
            confidence=0.0,
            audio_priority="default_ambient",
            reasoning="No text provided",
            genre_adjustments="No genre information available",
            emotional_arc="steady_state",
            atmospheric_qualities=[],
            sound_layers=[],
            trigger_words=[],
            ambient_suggestions=[]
        )

# Create a single instance for the app to use
smart_scene_classifier = SmartSceneClassifier()

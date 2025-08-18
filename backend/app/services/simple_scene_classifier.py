"""
Simple Scene Classification System
Config-driven, lightweight scene classifier that solves the Dracula problem
"""

import re
import yaml
from typing import Dict, Optional
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

class SceneContext(Enum):
    INDOOR = "indoor"
    OUTDOOR = "outdoor"
    URBAN = "urban"
    RURAL = "rural"
    NATURAL = "natural"
    BUILT = "built"

@dataclass
class SceneAnalysis:
    primary_scene: SceneType
    scene_context: SceneContext
    mood: str
    intensity: float
    confidence: float
    audio_priority: str
    reasoning: str
    genre_adjustments: str

class SimpleSceneClassifier:
    """
    Lightweight scene classifier that loads patterns from config files.
    Solves the Dracula problem with simple, maintainable logic.
    """
    
    def __init__(self):
        self.config_dir = Path(__file__).parent.parent.parent / "config"
        self.scene_patterns = self._load_scene_patterns()
        self.context_patterns = self._load_context_patterns()
        self.mood_patterns = self._load_mood_patterns()
        self.genre_adjustments = self._load_genre_adjustments()
    
    def _load_scene_patterns(self) -> Dict:
        """Load scene patterns from YAML config."""
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
    
    def classify_scene(self, text: str, genre: str = None) -> SceneAnalysis:
        """
        Analyze text and classify the scene with genre awareness.
        Simple, config-driven approach that solves the Dracula problem.
        """
        if not text or not text.strip():
            return self._create_neutral_analysis()
        
        # Step 1: Analyze scene types with pattern matching
        scene_scores = self._analyze_scene_types(text, genre)
        
        # Step 2: Determine primary scene type
        primary_scene = self._get_primary_scene(scene_scores)
        
        # Step 3: Analyze physical context
        scene_context = self._analyze_context(text)
        
        # Step 4: Analyze emotional mood
        mood = self._analyze_mood(text)
        
        # Step 5: Calculate intensity
        intensity = self._calculate_intensity(text, scene_scores, genre)
        
        # Step 6: Determine audio priority (SOLVES DRACULA PROBLEM)
        audio_priority = self._determine_audio_priority(primary_scene, text, genre)
        
        # Step 7: Generate reasoning
        reasoning = self._generate_reasoning(primary_scene, scene_scores, text, genre)
        
        # Step 8: Calculate confidence
        confidence = max(scene_scores.values()) if scene_scores else 0.0
        
        # Step 9: Generate genre adjustment explanation
        genre_adjustments = self._explain_genre_adjustments(genre, scene_scores)
        
        return SceneAnalysis(
            primary_scene=primary_scene,
            scene_context=scene_context,
            mood=mood,
            intensity=intensity,
            confidence=confidence,
            audio_priority=audio_priority,
            reasoning=reasoning,
            genre_adjustments=genre_adjustments
        )
    
    def _analyze_scene_types(self, text: str, genre: str = None) -> Dict[SceneType, float]:
        """Analyze scene types with genre-aware weight adjustments."""
        scene_scores = {}
        
        for scene_name, config in self.scene_patterns.items():
            scene_type = SceneType(scene_name)
            score = 0.0
            
            for pattern in config["patterns"]:
                matches = re.findall(pattern, text, re.IGNORECASE)
                score += len(matches) * config["base_weight"]
            
            # Apply genre-specific adjustments
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
    
    def _analyze_context(self, text: str) -> SceneContext:
        """Analyze the physical context of the scene."""
        context_scores = {}
        
        for context_name, patterns in self.context_patterns.items():
            context_type = SceneContext(context_name)
            score = 0.0
            
            for pattern in patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                score += len(matches)
            
            if score > 0:
                context_scores[context_type] = score
        
        if not context_scores:
            return SceneContext.INDOOR  # Default to indoor
        
        primary_context = max(context_scores.items(), key=lambda x: x[1])
        return primary_context[0]
    
    def _analyze_mood(self, text: str) -> str:
        """Analyze the emotional mood of the scene."""
        mood_scores = {}
        
        for mood, patterns in self.mood_patterns.items():
            score = 0.0
            for pattern in patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                score += len(matches)
            
            if score > 0:
                mood_scores[mood] = score
        
        if not mood_scores:
            return "neutral"
        
        primary_mood = max(mood_scores.items(), key=lambda x: x[1])
        return primary_mood[0]
    
    def _calculate_intensity(self, text: str, scene_scores: Dict[SceneType, float], genre: str = None) -> float:
        """Calculate the intensity level of the scene with genre awareness."""
        base_intensity = 0.5
        
        # Adjust based on scene type
        if SceneType.ACTION in scene_scores:
            base_intensity += 0.3
        if SceneType.EMOTIONAL in scene_scores:
            base_intensity += 0.2
        if SceneType.DIALOGUE in scene_scores:
            base_intensity += 0.1
        
        # Genre-specific intensity adjustments
        if genre and genre.lower() in self.genre_adjustments:
            if genre.lower() == "thriller":
                base_intensity += 0.2
            elif genre.lower() == "romance":
                base_intensity -= 0.1
            elif genre.lower() == "horror":
                base_intensity += 0.3
        
        # Adjust based on text length
        if len(text) > 200:
            base_intensity += 0.1
        
        return min(base_intensity, 1.0)
    
    def _determine_audio_priority(self, primary_scene: SceneType, text: str, genre: str = None) -> str:
        """
        Determine audio priority based on scene type, context, and genre.
        This is where we solve your Dracula problem with simple logic.
        """
        # Get base audio for scene type
        scene_name = primary_scene.value
        base_audio = self.scene_patterns[scene_name]["audio_base"]
        
        # For dialogue scenes - ALWAYS use conversation audio regardless of location mentions
        if primary_scene == SceneType.DIALOGUE:
            return "conversation_ambient"
        
        # For action scenes - ALWAYS use action audio regardless of location
        elif primary_scene == SceneType.ACTION:
            return "action_rhythms"
        
        # For emotional scenes - ALWAYS use emotional audio regardless of location
        elif primary_scene == SceneType.EMOTIONAL:
            return "emotional_ambient"
        
        # For transition scenes - ALWAYS use transition audio
        elif primary_scene == SceneType.TRANSITION:
            return "transition_ambient"
        
        # Only for descriptive scenes do we consider location-specific audio
        elif primary_scene == SceneType.DESCRIPTIVE:
            location_priority = self._get_location_priority(text, genre)
            if location_priority:
                return location_priority
        
        # Default to scene-based audio
        return base_audio
    
    def _get_location_priority(self, text: str, genre: str = None) -> Optional[str]:
        """Get location-specific audio with genre-aware priority adjustments."""
        text_lower = text.lower()
        
        # Base location priorities (hotel/dining takes highest priority)
        location_checks = [
            ("hotel", "dining", "restaurant"),  # Hotel/dining takes highest priority
            ("castle", "fortress", "palace"),   # Castle/fortress
            ("forest", "woods", "jungle"),      # Forest/nature
            ("mountain", "peak", "cliff"),      # Mountain/outdoor
            ("city", "town", "village"),        # Urban areas
            ("cave", "tunnel", "underground"),  # Underground
            ("storm", "rain", "weather"),       # Weather
        ]
        
        # Genre-specific adjustments
        if genre and genre.lower() == "fantasy":
            location_checks.insert(1, ("magic", "spell", "enchantment"))
        elif genre and genre.lower() == "horror":
            location_checks.insert(0, ("dark", "shadow", "night"))
        elif genre and genre.lower() == "sci-fi":
            location_checks.insert(0, ("spaceship", "lab", "technology"))
        
        # Check locations in priority order
        for location_group in location_checks:
            for location in location_group:
                if location in text_lower:
                    # Map to audio file names
                    if any(word in location_group for word in ["hotel", "dining", "restaurant"]):
                        return "hotel_dining_ambient"
                    elif any(word in location_group for word in ["castle", "fortress", "palace"]):
                        return "castle_atmosphere"
                    elif any(word in location_group for word in ["forest", "woods", "jungle"]):
                        return "forest_nature"
                    elif any(word in location_group for word in ["mountain", "peak", "cliff"]):
                        return "mountain_wind"
                    elif any(word in location_group for word in ["city", "town", "village"]):
                        return "urban_background"
                    elif any(word in location_group for word in ["cave", "tunnel", "underground"]):
                        return "cave_echoes"
                    elif any(word in location_group for word in ["storm", "rain", "weather"]):
                        return "storm_weather"
        
        return None
    
    def _generate_reasoning(self, primary_scene: SceneType, scene_scores: Dict[SceneType, float], text: str, genre: str = None) -> str:
        """Generate human-readable reasoning for the classification."""
        reasons = []
        
        # Primary scene reasoning
        reasons.append(f"Primary scene: {primary_scene.value}")
        
        # Score-based reasoning
        if scene_scores:
            top_scenes = sorted(scene_scores.items(), key=lambda x: x[1], reverse=True)[:3]
            for scene, score in top_scenes:
                reasons.append(f"{scene.value}: {score:.1f}")
        
        # Genre reasoning
        if genre:
            reasons.append(f"Genre: {genre} (adjusted weights applied)")
        
        # Context reasoning
        if "castle" in text.lower() and primary_scene != SceneType.DESCRIPTIVE:
            reasons.append("Castle mentioned but not primary scene - using scene-based audio")
        
        return " | ".join(reasons)
    
    def _explain_genre_adjustments(self, genre: str, scene_scores: Dict[SceneType, float]) -> str:
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
    
    def _create_neutral_analysis(self) -> SceneAnalysis:
        """Create a neutral analysis for empty text."""
        return SceneAnalysis(
            primary_scene=SceneType.NEUTRAL,
            scene_context=SceneContext.INDOOR,
            mood="neutral",
            intensity=0.0,
            confidence=0.0,
            audio_priority="default_ambient",
            reasoning="No text provided",
            genre_adjustments="No genre information available"
        )

# Create a single instance for the app to use
simple_scene_classifier = SimpleSceneClassifier()

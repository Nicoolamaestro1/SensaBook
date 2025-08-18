"""
Simple Smart Soundscape Service
Config-driven, lightweight soundscape service that solves the Dracula problem
"""

import yaml
import re
from typing import Dict, Optional, List
from sqlalchemy.orm import Session
from pathlib import Path
from .book import get_page, get_book
from .simple_scene_classifier import simple_scene_classifier, SceneAnalysis

class SimpleSmartSoundscapeService:
    """
    Lightweight soundscape service that loads mappings from config files.
    """
    
    def __init__(self):
        self.config_dir = Path(__file__).parent.parent.parent / "config"
        self.scene_audio_mapping = self._load_scene_audio_mapping()
        self.location_audio_mapping = self._load_location_audio_mapping()
        self.mood_audio_mapping = self._load_mood_audio_mapping()
        self.trigger_words = self._load_trigger_words()
    
    def _load_scene_audio_mapping(self) -> Dict:
        """Load scene audio mappings from YAML config."""
        config_file = self.config_dir / "audio_mappings.yaml"
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)
        return config["scene_audio_mapping"]
    
    def _load_location_audio_mapping(self) -> Dict:
        """Load location audio mappings from YAML config."""
        config_file = self.config_dir / "audio_mappings.yaml"
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)
        return config["location_audio_mapping"]
    
    def _load_mood_audio_mapping(self) -> Dict:
        """Load mood audio mappings from YAML config."""
        config_file = self.config_dir / "audio_mappings.yaml"
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)
        return config["mood_audio_mapping"]
    
    def _load_trigger_words(self) -> Dict:
        """Load trigger words from YAML config."""
        config_file = self.config_dir / "audio_mappings.yaml"
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)
        return config.get("trigger_words", {})
    
    def _detect_trigger_words(self, text: str) -> List[Dict]:
        """Detect trigger words in text and return their positions and sound files."""
        if not text or not self.trigger_words:
            return []
        
        triggers = []
        words = text.split()
        
        for i, word in enumerate(words):
            clean_word = re.sub(r'[^\w\s]', '', word.lower())
            
            # Check if this word is a trigger word
            if clean_word in self.trigger_words:
                trigger_info = self.trigger_words[clean_word]
                triggers.append({
                    "word": clean_word,
                    "position": i,
                    "file": trigger_info.get("sound", f"{clean_word}.mp3")
                })
        
        return triggers
    
    def _get_carpet_tracks(self, scene_analysis: SceneAnalysis) -> List[str]:
        """Get carpet tracks (ambient background) based on scene analysis."""
        primary_audio = self._get_primary_audio(scene_analysis)
        secondary_audio = self._get_secondary_audio(scene_analysis, primary_audio)
        
        # Return both primary and secondary as carpet tracks
        return [primary_audio, secondary_audio]
    
    def generate_smart_soundscape(self, text: str, book_id: int = None, chapter_number: int = None, page_number: int = None, genre: str = None) -> Dict:
        """
        Generate intelligent soundscape based on scene classification.
        This solves the Dracula problem by understanding scene context.
        """
        if not text or not text.strip():
            return self._create_default_soundscape()
        
        # Step 1: Analyze the scene using our simple classifier
        scene_analysis = simple_scene_classifier.classify_scene(text, genre)
        
        # Step 2: Get primary audio based on scene type
        primary_audio = self._get_primary_audio(scene_analysis)
        
        # Step 3: Get secondary audio for variety
        secondary_audio = self._get_secondary_audio(scene_analysis, primary_audio)
        
        # Step 4: Detect trigger words
        trigger_words = self._detect_trigger_words(text)
        
        # Step 5: Get carpet tracks
        carpet_tracks = self._get_carpet_tracks(scene_analysis)
        
        # Step 6: Generate comprehensive soundscape
        soundscape = {
            "primary_audio": primary_audio,
            "secondary_audio": secondary_audio,
            "scene_type": scene_analysis.primary_scene.value,
            "scene_context": scene_analysis.scene_context.value,
            "mood": scene_analysis.mood,
            "intensity": scene_analysis.intensity,
            "confidence": scene_analysis.confidence,
            "reasoning": scene_analysis.reasoning,
            "audio_priority": scene_analysis.audio_priority,
            "genre": genre,
            "genre_adjustments": scene_analysis.genre_adjustments,
            "book_id": book_id,
            "chapter_number": chapter_number,
            "page_number": page_number,
            # Trigger words functionality
            "triggered_sounds": trigger_words,
            "carpet_tracks": carpet_tracks
        }
        
        return soundscape
    
    def _get_primary_audio(self, scene_analysis: SceneAnalysis) -> str:
        """Get the primary audio file based on scene analysis."""
        scene_type = scene_analysis.primary_scene.value
        
        # Get base audio for scene type
        if scene_type in self.scene_audio_mapping:
            base_audio = self.scene_audio_mapping[scene_type]["primary"]
        else:
            base_audio = "default_ambient"
        
        # For descriptive scenes, check if we should override with location-specific audio
        if scene_type == "descriptive":
            location_audio = self._get_location_specific_audio(scene_analysis)
            if location_audio:
                return location_audio
        
        return base_audio
    
    def _get_location_specific_audio(self, scene_analysis: SceneAnalysis) -> Optional[str]:
        """Get location-specific audio only for descriptive scenes."""
        # This is where we solve your Dracula problem
        # Only use location audio for descriptive scenes, not for dialogue/action
        
        # Use the audio_priority from scene_classifier which already handles this logic correctly
        priority = scene_analysis.audio_priority
        
        # Map the audio_priority to our actual audio files
        audio_mapping = {
            "hotel_dining_ambient": "hotel_dining_ambient",
            "castle_atmosphere": "castle_atmosphere",
            "forest_nature": "forest_nature",
            "mountain_wind": "mountain_wind",
            "urban_background": "urban_background",
            "small_town_ambient": "small_town_ambient",
            "cave_echoes": "cave_echoes",
            "storm_weather": "storm_weather",
            "rain_ambient": "rain_ambient",
            "default_ambient": "default_ambient"
        }
        
        if priority in audio_mapping:
            return audio_mapping[priority]
        
        return None
    
    def _get_secondary_audio(self, scene_analysis: SceneAnalysis, primary_audio: str) -> str:
        """Get secondary audio for variety and depth."""
        scene_type = scene_analysis.primary_scene.value
        
        if scene_type in self.scene_audio_mapping:
            alternatives = self.scene_audio_mapping[scene_type]["alternatives"]
            # Pick first alternative that's different from primary
            for alt in alternatives:
                if alt != primary_audio:
                    return alt
        
        # Fallback to mood-based audio
        if scene_analysis.mood in self.mood_audio_mapping:
            mood_audio = self.mood_audio_mapping[scene_analysis.mood]
            if mood_audio != primary_audio:
                return mood_audio
        
        return "gentle_atmosphere"  # Default secondary audio
    
    def _create_default_soundscape(self) -> Dict:
        """Create a default soundscape for empty text."""
        return {
            "primary_audio": "default_ambient",
            "secondary_audio": "gentle_atmosphere",
            "scene_type": "neutral",
            "scene_context": "indoor",
            "mood": "neutral",
            "intensity": 0.0,
            "confidence": 0.0,
            "reasoning": "No text provided",
            "audio_priority": "default_ambient",
            "genre": None,
            "genre_adjustments": "No genre information available",
            "book_id": None,
            "chapter_number": None,
            "page_number": None
        }
    
    def get_soundscape_for_page(self, book_id: int, chapter_number: int, page_number: int, db: Session) -> Dict:
        """
        Get soundscape for a specific book page using scene classification.
        """
        try:
            # Get the page content
            book_page = get_page(book_id=book_id, chapter_number=chapter_number, page_number=page_number, db=db)
            if not book_page:
                return {"error": "Book page not found"}
            
            # Get the book information to extract genre
            book_info = get_book(book_id=book_id, db=db)
            genre = book_info.genre if book_info else None
            
            # Generate smart soundscape with genre information
            soundscape = self.generate_smart_soundscape(
                text=book_page.content,
                book_id=book_id,
                chapter_number=chapter_number,
                page_number=page_number,
                genre=genre
            )
            
            return soundscape
            
        except Exception as e:
            return {
                "error": f"Failed to generate soundscape: {str(e)}",
                "fallback_audio": "default_ambient"
            }
    
    def analyze_text_scene(self, text: str, genre: str = None) -> Dict:
        """
        Analyze text and return scene classification with audio recommendations.
        Useful for testing and debugging.
        """
        scene_analysis = simple_scene_classifier.classify_scene(text, genre)
        
        return {
            "scene_analysis": {
                "primary_scene": scene_analysis.primary_scene.value,
                "scene_context": scene_analysis.scene_context.value,
                "mood": scene_analysis.mood,
                "intensity": scene_analysis.intensity,
                "confidence": scene_analysis.confidence,
                "reasoning": scene_analysis.reasoning,
                "genre_adjustments": scene_analysis.genre_adjustments
            },
            "audio_recommendations": {
                "primary": self._get_primary_audio(scene_analysis),
                "secondary": self._get_secondary_audio(scene_analysis, self._get_primary_audio(scene_analysis)),
                "priority": scene_analysis.audio_priority
            },
            "explanation": f"Scene classified as {scene_analysis.primary_scene.value} with {scene_analysis.confidence:.2f} confidence. {scene_analysis.reasoning}",
            "genre_intelligence": f"Genre '{genre}' applied: {scene_analysis.genre_adjustments}" if genre else "No genre information provided"
        }

# Create a single instance for the app to use
simple_smart_soundscape_service = SimpleSmartSoundscapeService()

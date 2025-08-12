from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import logging
from .ai_emotion_analysis import ai_emotion_analyzer, AIEmotionResult
from .emotion_analysis import emotion_analyzer
from .soundscape import find_trigger_words, ENHANCED_SCENE_SOUND_MAPPINGS

# Set up logging
logger = logging.getLogger(__name__)

@dataclass
class AISoundscapeResult:
    """Result from AI-enhanced soundscape generation."""
    primary_soundscape: str
    secondary_soundscape: str
    intensity: float
    atmosphere: str
    recommended_volume: float
    sound_effects: List[str]
    ai_confidence: float
    ai_emotion: str
    fallback_used: bool
    trigger_words: List[Dict]
    metadata: Dict[str, Any]

class AIEnhancedSoundscapeService:
    """
    AI-enhanced soundscape service that combines AI emotion analysis
    with existing soundscape generation logic.
    
    This service maintains 100% API compatibility with the existing system
    while providing AI-powered enhancements when available.
    """
    
    def __init__(self):
        """Initialize the AI-enhanced soundscape service."""
        self.ai_enabled = True
        self.confidence_threshold = 0.7
        self.fallback_enabled = True
        
        # Audio mapping based on AI confidence levels
        self.confidence_audio_mapping = {
            "high": {  # 0.9+
                "volume_multiplier": 1.2,
                "intensity_boost": 1.3,
                "effect_density": "high"
            },
            "medium": {  # 0.7-0.9
                "volume_multiplier": 1.0,
                "intensity_boost": 1.0,
                "effect_density": "medium"
            },
            "low": {  # 0.5-0.7
                "volume_multiplier": 0.8,
                "intensity_boost": 0.7,
                "effect_density": "low"
            },
            "very_low": {  # <0.5
                "volume_multiplier": 0.6,
                "intensity_boost": 0.5,
                "effect_density": "minimal"
            }
        }
    
    def generate_soundscape(self, text: str, use_ai: bool = True) -> AISoundscapeResult:
        """
        Generate soundscape using AI-enhanced analysis.
        
        Args:
            text: The text to analyze
            use_ai: Whether to use AI analysis (default: True)
            
        Returns:
            AISoundscapeResult with enhanced soundscape recommendations
        """
        try:
            if use_ai and self.ai_enabled:
                return self._generate_ai_soundscape(text)
            else:
                return self._generate_fallback_soundscape(text)
                
        except Exception as e:
            logger.error(f"Error in AI-enhanced soundscape generation: {e}")
            if self.fallback_enabled:
                logger.info("Falling back to rule-based system")
                return self._generate_fallback_soundscape(text)
            else:
                raise
    
    def _generate_ai_soundscape(self, text: str) -> AISoundscapeResult:
        """Generate soundscape using AI emotion analysis."""
        logger.info("Generating AI-enhanced soundscape")
        
        # Get AI emotion analysis
        ai_result = ai_emotion_analyzer.analyze_emotion(text)
        
        # Get trigger words using existing system
        trigger_words = find_trigger_words(text)
        
        # Determine confidence level for audio mapping
        confidence_level = self._get_confidence_level(ai_result.confidence)
        audio_config = self.confidence_audio_mapping[confidence_level]
        
        # Generate soundscape using AI results
        primary_soundscape = self._map_ai_emotion_to_soundscape(ai_result)
        secondary_soundscape = self._map_ai_theme_to_soundscape(ai_result, text)
        
        # Calculate enhanced intensity and volume
        intensity = self._calculate_ai_intensity(ai_result, audio_config)
        volume = self._calculate_ai_volume(ai_result, audio_config)
        
        # Generate sound effects based on AI confidence
        sound_effects = self._generate_ai_sound_effects(ai_result, trigger_words, audio_config)
        
        # Determine atmosphere
        atmosphere = self._determine_ai_atmosphere(ai_result, text)
        
        # Create metadata for debugging and optimization
        metadata = {
            "ai_model_used": "j-hartmann/emotion-english-distilroberta-base",
            "confidence_level": confidence_level,
            "audio_config": audio_config,
            "emotion_scores": ai_result.emotion_scores,
            "raw_predictions": ai_result.raw_predictions,
            "context_embeddings": ai_result.context_embeddings
        }
        
        return AISoundscapeResult(
            primary_soundscape=primary_soundscape,
            secondary_soundscape=secondary_soundscape,
            intensity=intensity,
            atmosphere=atmosphere,
            recommended_volume=volume,
            sound_effects=sound_effects,
            ai_confidence=ai_result.confidence,
            ai_emotion=ai_result.primary_emotion.value,
            fallback_used=False,
            trigger_words=trigger_words,
            metadata=metadata
        )
    
    def _generate_fallback_soundscape(self, text: str) -> AISoundscapeResult:
        """Generate soundscape using the existing rule-based system."""
        logger.info("Generating fallback soundscape using rule-based system")
        
        # Use existing emotion analyzer
        emotion_result = emotion_analyzer.analyze_emotion(text)
        theme_result = emotion_analyzer.analyze_theme(text)
        
        # Get trigger words
        trigger_words = find_trigger_words(text)
        
        # Generate soundscape using existing logic
        soundscape_recs = emotion_analyzer.generate_soundscape_recommendations(
            emotion_result, theme_result
        )
        
        # Create metadata for fallback tracking
        metadata = {
            "fallback_reason": "AI unavailable or disabled",
            "rule_based_emotion": emotion_result.primary_emotion.value,
            "rule_based_intensity": emotion_result.intensity,
            "rule_based_confidence": emotion_result.confidence
        }
        
        return AISoundscapeResult(
            primary_soundscape=soundscape_recs.get("primary_soundscape", "default_ambience.mp3"),
            secondary_soundscape=soundscape_recs.get("secondary_soundscape", "default_ambience.mp3"),
            intensity=soundscape_recs.get("intensity", 0.5),
            atmosphere=soundscape_recs.get("atmosphere", "neutral"),
            recommended_volume=soundscape_recs.get("recommended_volume", 0.5),
            sound_effects=soundscape_recs.get("sound_effects", []),
            ai_confidence=0.0,
            ai_emotion="fallback",
            fallback_used=True,
            trigger_words=trigger_words,
            metadata=metadata
        )
    
    def _get_confidence_level(self, confidence: float) -> str:
        """Determine confidence level for audio mapping."""
        if confidence >= 0.9:
            return "high"
        elif confidence >= 0.7:
            return "medium"
        elif confidence >= 0.5:
            return "low"
        else:
            return "very_low"
    
    def _map_ai_emotion_to_soundscape(self, ai_result: AIEmotionResult) -> str:
        """Map AI emotion result to soundscape file."""
        emotion_mapping = {
            "joy": "bright_ambience.mp3",
            "sadness": "melancholy_drones.mp3",
            "anger": "tense_rhythms.mp3",
            "fear": "dark_ambience.mp3",
            "surprise": "sudden_impact.mp3",
            "disgust": "unsettling_tones.mp3",
            "neutral": "default_ambience.mp3"
        }
        
        return emotion_mapping.get(ai_result.primary_emotion.value, "default_ambience.mp3")
    
    def _map_ai_theme_to_soundscape(self, ai_result: AIEmotionResult, text: str) -> str:
        """Map AI analysis to theme-based soundscape."""
        # Use existing theme detection for now
        theme_result = emotion_analyzer.analyze_theme(text)
        
        theme_mapping = {
            "adventure": "epic_journey.mp3",
            "romance": "romantic_melody.mp3",
            "mystery": "mysterious_ambience.mp3",
            "horror": "horror_ambience.mp3",
            "fantasy": "magical_realms.mp3",
            "drama": "dramatic_tension.mp3",
            "comedy": "light_hearted.mp3",
            "action": "action_rhythms.mp3"
        }
        
        return theme_mapping.get(theme_result.primary_theme.value, "default_ambience.mp3")
    
    def _calculate_ai_intensity(self, ai_result: AIEmotionResult, audio_config: Dict) -> float:
        """Calculate enhanced intensity using AI confidence and audio config."""
        base_intensity = ai_result.confidence
        
        # Apply intensity boost based on confidence level
        intensity_boost = audio_config.get("intensity_boost", 1.0)
        enhanced_intensity = base_intensity * intensity_boost
        
        # Ensure intensity stays within bounds
        return min(max(enhanced_intensity, 0.0), 1.0)
    
    def _calculate_ai_volume(self, ai_result: AIEmotionResult, audio_config: Dict) -> float:
        """Calculate enhanced volume using AI confidence and audio config."""
        base_volume = 0.5
        
        # Apply volume multiplier based on confidence level
        volume_multiplier = audio_config.get("volume_multiplier", 1.0)
        enhanced_volume = base_volume * volume_multiplier
        
        # Ensure volume stays within bounds
        return min(max(enhanced_volume, 0.0), 1.0)
    
    def _generate_ai_sound_effects(self, ai_result: AIEmotionResult, 
                                 trigger_words: List[Dict], 
                                 audio_config: Dict) -> List[str]:
        """Generate sound effects based on AI analysis and confidence."""
        effects = []
        
        # Add emotion-based effects
        emotion = ai_result.primary_emotion.value
        if emotion == "fear":
            effects.extend(["heartbeat.mp3", "distant_scream.mp3"])
        elif emotion == "surprise":
            effects.append("sudden_impact.mp3")
        elif emotion == "joy":
            effects.append("bright_chimes.mp3")
        elif emotion == "anger":
            effects.append("tension_rise.mp3")
        elif emotion == "sadness":
            effects.append("gentle_sigh.mp3")
        
        # Add trigger-based effects based on confidence level
        effect_density = audio_config.get("effect_density", "medium")
        
        if effect_density == "high":
            # Include all relevant trigger words
            for trigger in trigger_words[:5]:  # Top 5 triggers
                if "sound" in trigger:
                    effects.append(trigger["sound"])
        elif effect_density == "medium":
            # Include moderate number of effects
            for trigger in trigger_words[:3]:  # Top 3 triggers
                if "sound" in trigger:
                    effects.append(trigger["sound"])
        elif effect_density == "low":
            # Include minimal effects
            for trigger in trigger_words[:1]:  # Top 1 trigger
                if "sound" in trigger:
                    effects.append(trigger["sound"])
        # "minimal" density gets no additional effects
        
        return list(set(effects))  # Remove duplicates
    
    def _determine_ai_atmosphere(self, ai_result: AIEmotionResult, text: str) -> str:
        """Determine atmosphere using AI analysis and text context."""
        # Use existing atmosphere detection
        theme_result = emotion_analyzer.analyze_theme(text)
        base_atmosphere = theme_result.atmosphere
        
        # Enhance atmosphere based on AI confidence
        if ai_result.confidence > 0.8:
            # High confidence - use AI emotion to enhance atmosphere
            emotion = ai_result.primary_emotion.value
            if emotion == "fear":
                return "dark" if base_atmosphere == "neutral" else base_atmosphere
            elif emotion == "joy":
                return "bright" if base_atmosphere == "neutral" else base_atmosphere
            elif emotion == "anger":
                return "tense" if base_atmosphere == "neutral" else base_atmosphere
        
        return base_atmosphere
    
    def batch_generate_soundscapes(self, texts: List[str], use_ai: bool = True) -> List[AISoundscapeResult]:
        """Generate soundscapes for multiple texts efficiently."""
        results = []
        for i, text in enumerate(texts):
            logger.info(f"Generating soundscape {i+1}/{len(texts)}")
            result = self.generate_soundscape(text, use_ai)
            results.append(result)
        return results
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get performance metrics for the AI-enhanced system."""
        return {
            "ai_enabled": self.ai_enabled,
            "fallback_enabled": self.fallback_enabled,
            "confidence_threshold": self.confidence_threshold,
            "audio_configs": self.confidence_audio_mapping,
            "system_status": "operational"
        }

# Global AI-enhanced soundscape service instance
ai_soundscape_service = AIEnhancedSoundscapeService()

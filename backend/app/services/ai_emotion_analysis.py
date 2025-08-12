from transformers import pipeline
import numpy as np
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EmotionType(Enum):
    JOY = "joy"
    SADNESS = "sadness"
    ANGER = "anger"
    FEAR = "fear"
    SURPRISE = "surprise"
    DISGUST = "disgust"
    NEUTRAL = "neutral"

@dataclass
class AIEmotionResult:
    primary_emotion: EmotionType
    emotion_scores: Dict[str, float]
    confidence: float
    context_embeddings: List[float]
    raw_predictions: Dict[str, float]
    text_analyzed: str

class AIEmotionAnalyzer:
    def __init__(self):
        """Initialize the AI-powered emotion analyzer."""
        try:
            logger.info("Initializing AI Emotion Analyzer...")
            
            # Use a pre-trained emotion classifier
            self.emotion_classifier = pipeline(
                "text-classification",
                model="j-hartmann/emotion-english-distilroberta-base",
                return_all_scores=True
            )
            
            # Emotion mapping from the model's output to your system
            self.emotion_mapping = {
                "joy": EmotionType.JOY,
                "sadness": EmotionType.SADNESS,
                "anger": EmotionType.ANGER,
                "fear": EmotionType.FEAR,
                "surprise": EmotionType.SURPRISE,
                "disgust": EmotionType.DISGUST,
                "neutral": EmotionType.NEUTRAL
            }
            
            # Reverse mapping for debugging
            self.reverse_mapping = {v: k for k, v in self.emotion_mapping.items()}
            
            logger.info("AI Emotion Analyzer initialized successfully!")
            
        except Exception as e:
            logger.error(f"Failed to initialize AI Emotion Analyzer: {e}")
            raise
    
    def analyze_emotion(self, text: str) -> AIEmotionResult:
        """
        Analyze emotion using AI model instead of rules.
        
        Args:
            text: The text to analyze
            
        Returns:
            AIEmotionResult with AI-generated emotion analysis
        """
        if not text or not text.strip():
            return AIEmotionResult(
                primary_emotion=EmotionType.NEUTRAL,
                emotion_scores={},
                confidence=0.0,
                context_embeddings=[],
                raw_predictions={},
                text_analyzed=text
            )
        
        try:
            logger.info(f"Analyzing emotion for text: {text[:100]}...")
            
            # Get AI predictions
            predictions = self.emotion_classifier(text)
            
            # Extract emotion scores
            emotion_scores = {}
            raw_predictions = {}
            
            for pred in predictions[0]:
                emotion = pred['label']
                score = pred['score']
                raw_predictions[emotion] = score
                
                # Map to your emotion system if possible
                if emotion in self.emotion_mapping:
                    mapped_emotion = self.emotion_mapping[emotion]
                    emotion_scores[mapped_emotion.value] = score
                else:
                    # Handle unmapped emotions by adding them with original names
                    emotion_scores[emotion] = score
            
            # Find primary emotion
            if emotion_scores:
                primary_emotion_key = max(emotion_scores.items(), key=lambda x: x[1])
                primary_emotion_value = primary_emotion_key[0]
                
                # Try to map back to EmotionType enum
                try:
                    primary_emotion = EmotionType(primary_emotion_value)
                except ValueError:
                    # If it's not in our enum, create a neutral result
                    primary_emotion = EmotionType.NEUTRAL
                    logger.warning(f"Unknown emotion type: {primary_emotion_value}, defaulting to neutral")
                
                confidence = primary_emotion_key[1]
            else:
                primary_emotion = EmotionType.NEUTRAL
                confidence = 0.0
            
            # Create context embeddings (placeholder for now - we'll enhance this later)
            context_embeddings = self._generate_context_embeddings(text)
            
            result = AIEmotionResult(
                primary_emotion=primary_emotion,
                emotion_scores=emotion_scores,
                confidence=confidence,
                context_embeddings=context_embeddings,
                raw_predictions=raw_predictions,
                text_analyzed=text
            )
            
            logger.info(f"Analysis complete: {primary_emotion.value} (confidence: {confidence:.3f})")
            return result
            
        except Exception as e:
            logger.error(f"Error in emotion analysis: {e}")
            # Return neutral result on error
            return AIEmotionResult(
                primary_emotion=EmotionType.NEUTRAL,
                emotion_scores={},
                confidence=0.0,
                context_embeddings=[],
                raw_predictions={},
                text_analyzed=text
            )
    
    def batch_analyze(self, texts: List[str]) -> List[AIEmotionResult]:
        """
        Analyze multiple texts efficiently.
        
        Args:
            texts: List of texts to analyze
            
        Returns:
            List of AIEmotionResult objects
        """
        results = []
        for i, text in enumerate(texts):
            logger.info(f"Processing text {i+1}/{len(texts)}")
            result = self.analyze_emotion(text)
            results.append(result)
        return results
    
    def _generate_context_embeddings(self, text: str) -> List[float]:
        """
        Generate context embeddings for the text.
        This is a placeholder that we'll enhance with sentence transformers later.
        
        Args:
            text: The text to embed
            
        Returns:
            List of embedding values (placeholder for now)
        """
        # For now, return a simple feature vector based on text characteristics
        # We'll replace this with proper sentence embeddings in the next phase
        
        features = [
            len(text) / 1000.0,  # Normalized text length
            text.count('!') / max(len(text.split()), 1),  # Exclamation density
            text.count('?') / max(len(text.split()), 1),  # Question density
            text.count('.') / max(len(text.split()), 1),  # Sentence density
            sum(1 for c in text if c.isupper()) / max(len(text), 1),  # Capitalization ratio
        ]
        
        return features
    
    def get_emotion_intensity(self, emotion_result: AIEmotionResult) -> float:
        """
        Calculate emotion intensity based on AI confidence and scores.
        
        Args:
            emotion_result: The AI emotion analysis result
            
        Returns:
            Intensity value between 0.0 and 1.0
        """
        if not emotion_result.emotion_scores:
            return 0.0
        
        # Use the confidence as a base intensity
        base_intensity = emotion_result.confidence
        
        # Boost intensity if multiple emotions are detected
        emotion_count = len(emotion_result.emotion_scores)
        if emotion_count > 1:
            # Calculate variance in emotion scores
            scores = list(emotion_result.emotion_scores.values())
            variance = np.var(scores) if len(scores) > 1 else 0.0
            
            # Higher variance means more complex emotional content
            complexity_boost = min(variance * 0.5, 0.3)
            base_intensity += complexity_boost
        
        return min(base_intensity, 1.0)
    
    def compare_with_rule_based(self, text: str, rule_based_result) -> Dict:
        """
        Compare AI results with rule-based results for validation.
        
        Args:
            text: The analyzed text
            rule_based_result: Result from the old rule-based system
            
        Returns:
            Dictionary with comparison metrics
        """
        ai_result = self.analyze_emotion(text)
        
        comparison = {
            "text": text[:100] + "..." if len(text) > 100 else text,
            "ai_emotion": ai_result.primary_emotion.value,
            "ai_confidence": ai_result.confidence,
            "rule_based_emotion": getattr(rule_based_result, 'primary_emotion', {}).value if hasattr(rule_based_result, 'primary_emotion') else "unknown",
            "agreement": ai_result.primary_emotion.value == getattr(rule_based_result, 'primary_emotion', {}).value if hasattr(rule_based_result, 'primary_emotion') else False,
            "ai_scores": ai_result.emotion_scores,
            "raw_predictions": ai_result.raw_predictions
        }
        
        return comparison

# Global AI analyzer instance
ai_emotion_analyzer = AIEmotionAnalyzer()

#!/usr/bin/env python3
"""
Combines mood analysis and emotion analysis to provide complete soundscape recommendations for book pages.
"""

from typing import Dict, List, Any
from app.services.mood_analyzer import AdvancedMoodAnalyzer
from app.services.emotion_analysis import AdvancedEmotionAnalyzer, find_trigger_words

class PageAnalyzer:
    """Combines mood analysis, emotion analysis, and theme analysis for complete page sound analysis"""

    def __init__(self):
        self.mood_analyzer = AdvancedMoodAnalyzer()  # Updated to use AdvancedMoodAnalyzer
        self.emotion_analyzer = AdvancedEmotionAnalyzer()

    def analyze_page_complete(self, text: str) -> Dict[str, Any]:
        """
        Performs complete analysis of a page using all three analysis methods.
        
        Args:
            text: The page content to analyze
            
        Returns:
            Dictionary containing comprehensive analysis results
        """
        # Step 1: Analyze mood for carpet sound
        mood_analysis = self.mood_analyzer.analyze_page_mood(text)

        # Step 2: Analyze emotion and theme
        emotion_analysis = self.emotion_analyzer.analyze_emotion(text)
        theme_analysis = self.emotion_analyzer.analyze_theme(text)

        # Step 3: Find trigger words
        trigger_words = find_trigger_words(text)

        # Step 4: Generate soundscape recommendations from emotion/theme analysis
        soundscape_recommendations = self.emotion_analyzer.generate_soundscape_recommendations(
            emotion_analysis, theme_analysis
        )

        # Step 5: Calculate overall confidence
        overall_confidence = self._calculate_overall_confidence(
            mood_analysis, emotion_analysis, theme_analysis, trigger_words
        )

        # Step 6: Generate combined reasoning
        combined_reasoning = self._generate_combined_reasoning(
            mood_analysis, emotion_analysis, theme_analysis, trigger_words
        )

        return {
            "carpet_sound": mood_analysis.suggested_sound,
            "trigger_words": trigger_words,
            "mood_analysis": mood_analysis,
            "emotion_analysis": emotion_analysis,
            "theme_analysis": theme_analysis,
            "soundscape_recommendations": soundscape_recommendations,
            "confidence": overall_confidence,
            "reasoning": combined_reasoning,
            "primary_mood": mood_analysis.primary_mood,
            "secondary_mood": mood_analysis.secondary_mood,
            "primary_emotion": emotion_analysis.primary_emotion.value,
            "primary_theme": theme_analysis.primary_theme.value,
            "emotion_intensity": emotion_analysis.intensity,
            "atmosphere": theme_analysis.atmosphere,
            "context_phrases": mood_analysis.context_phrases,
            "emotional_intensity": mood_analysis.emotional_intensity,
            "atmospheric_density": mood_analysis.atmospheric_density
        }

    def analyze_book_pages_complete(self, book_content: List[str]) -> List[Dict[str, Any]]:
        """
        Analyzes all pages of a book with complete analysis.
        
        Args:
            book_content: List of page content strings
            
        Returns:
            List of complete analysis dictionaries for each page
        """
        analyses = []
        
        for i, page_content in enumerate(book_content, 1):
            analysis = self.analyze_page_complete(page_content)
            analyses.append(analysis)
            print(f"Page {i}: {analysis['primary_mood']} -> {analysis['carpet_sound']} (confidence: {analysis['confidence']:.2f})")
        
        return analyses

    def _calculate_overall_confidence(self, mood_analysis, emotion_analysis, theme_analysis, trigger_words) -> float:
        """Calculate overall confidence combining all analysis methods"""
        
        # Mood confidence (40% weight)
        mood_confidence = mood_analysis.confidence
        
        # Emotion confidence (30% weight)
        emotion_confidence = emotion_analysis.confidence
        
        # Theme confidence (20% weight)
        theme_confidence = theme_analysis.confidence
        
        # Trigger words confidence (10% weight)
        trigger_confidence = min(len(trigger_words) / 5.0, 1.0)
        
        # Weighted average
        overall_confidence = (
            mood_confidence * 0.4 +
            emotion_confidence * 0.3 +
            theme_confidence * 0.2 +
            trigger_confidence * 0.1
        )
        
        return min(1.0, overall_confidence)

    def _generate_combined_reasoning(self, mood_analysis, emotion_analysis, theme_analysis, trigger_words) -> str:
        """Generate comprehensive reasoning combining all analysis methods"""
        
        reasons = []
        
        # Mood reasoning
        reasons.append(f"Mood: {mood_analysis.primary_mood} ({mood_analysis.reasoning})")
        
        # Emotion reasoning
        reasons.append(f"Emotion: {emotion_analysis.primary_emotion.value} (intensity: {emotion_analysis.intensity:.2f})")
        
        # Theme reasoning
        reasons.append(f"Theme: {theme_analysis.primary_theme.value} (atmosphere: {theme_analysis.atmosphere})")
        
        # Trigger words reasoning
        if trigger_words:
            reasons.append(f"Trigger words: {len(trigger_words)} detected")
        
        return "; ".join(reasons)

    def get_soundscape_recommendation(self, text: str) -> Dict[str, Any]:
        """
        Formats the complete analysis into a soundscape recommendation for the frontend.
        
        Args:
            text: The page content to analyze
            
        Returns:
            Dictionary formatted for frontend consumption
        """
        analysis = self.analyze_page_complete(text)
        
        return {
            "carpet_tracks": [analysis["carpet_sound"]],
            "triggered_sounds": analysis["trigger_words"],
            "mood": analysis["primary_mood"],
            "emotion": analysis["primary_emotion"],
            "theme": analysis["primary_theme"],
            "intensity": analysis["emotion_intensity"],
            "atmosphere": analysis["atmosphere"],
            "confidence": analysis["confidence"],
            "reasoning": analysis["reasoning"],
            "soundscape_recommendations": analysis["soundscape_recommendations"],
            "context_phrases": analysis["context_phrases"],
            "emotional_intensity": analysis["emotional_intensity"],
            "atmospheric_density": analysis["atmospheric_density"]
        }

# Convenience functions
def analyze_page_complete(text: str) -> Dict[str, Any]:
    """Convenience function for complete page analysis"""
    analyzer = PageAnalyzer()
    return analyzer.analyze_page_complete(text)

def get_soundscape_recommendation(text: str) -> Dict[str, Any]:
    """Convenience function for soundscape recommendation"""
    analyzer = PageAnalyzer()
    return analyzer.get_soundscape_recommendation(text) 
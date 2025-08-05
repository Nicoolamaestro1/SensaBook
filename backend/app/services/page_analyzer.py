"""
Combined page analyzer that uses both mood analysis and emotion analysis
to provide complete soundscape recommendations for book pages.
"""

from typing import Dict, List, Any
from app.services.mood_analyzer import MoodAnalyzer, MoodAnalysis
from app.services.emotion_analysis import find_trigger_words, TRIGGER_WORDS

class PageAnalyzer:
    """Combines mood analysis and emotion analysis for complete page sound analysis"""
    
    def __init__(self):
        self.mood_analyzer = MoodAnalyzer()
    
    def analyze_page_complete(self, text: str) -> Dict[str, Any]:
        """
        Performs complete analysis of a page, returning both carpet sound and trigger words.
        
        Args:
            text: The page content to analyze
            
        Returns:
            Dictionary containing:
            - carpet_sound: Suggested ambient sound for the page
            - trigger_words: List of trigger words with timing
            - mood_analysis: Complete mood analysis object
            - confidence: Overall confidence in the analysis
            - reasoning: Combined reasoning for the recommendations
        """
        # Step 1: Analyze mood for carpet sound
        mood_analysis = self.mood_analyzer.analyze_page_mood(text)
        
        # Step 2: Find trigger words
        trigger_words = find_trigger_words(text)
        
        # Step 3: Calculate overall confidence
        overall_confidence = self._calculate_overall_confidence(mood_analysis, trigger_words)
        
        # Step 4: Generate combined reasoning
        combined_reasoning = self._generate_combined_reasoning(mood_analysis, trigger_words)
        
        return {
            "carpet_sound": mood_analysis.suggested_sound,
            "trigger_words": trigger_words,
            "mood_analysis": mood_analysis,
            "confidence": overall_confidence,
            "reasoning": combined_reasoning,
            "primary_mood": mood_analysis.primary_mood,
            "secondary_mood": mood_analysis.secondary_mood
        }
    
    def analyze_book_pages_complete(self, book_content: List[str]) -> List[Dict[str, Any]]:
        """
        Analyzes all pages of a book and returns complete analysis for each page.
        
        Args:
            book_content: List of page content strings
            
        Returns:
            List of complete analysis dictionaries for each page
        """
        analyses = []
        
        for i, page_content in enumerate(book_content, 1):
            analysis = self.analyze_page_complete(page_content)
            analysis["page_number"] = i
            
            # Print summary for each page
            print(f"Page {i}: {analysis['primary_mood']} -> {analysis['carpet_sound']} "
                  f"({len(analysis['trigger_words'])} triggers, confidence: {analysis['confidence']:.2f})")
            
            analyses.append(analysis)
        
        return analyses
    
    def _calculate_overall_confidence(self, mood_analysis: MoodAnalysis, trigger_words: List[Dict]) -> float:
        """Calculates overall confidence based on both mood and trigger word analysis"""
        
        # Base confidence from mood analysis
        mood_confidence = mood_analysis.confidence
        
        # Boost confidence if we found trigger words
        trigger_boost = min(0.3, len(trigger_words) * 0.1)
        
        # Higher confidence if we have both mood and triggers
        if mood_confidence > 0.5 and trigger_words:
            trigger_boost += 0.1
        
        overall_confidence = min(1.0, mood_confidence + trigger_boost)
        
        return overall_confidence
    
    def _generate_combined_reasoning(self, mood_analysis: MoodAnalysis, trigger_words: List[Dict]) -> str:
        """Generates combined reasoning for both mood and trigger word analysis"""
        
        reasons = []
        
        # Add mood reasoning
        if mood_analysis.primary_mood != "neutral":
            reasons.append(f"Atmosphere: {mood_analysis.primary_mood} ({mood_analysis.reasoning})")
        
        # Add trigger word reasoning
        if trigger_words:
            trigger_words_list = [tw["word"] for tw in trigger_words]
            reasons.append(f"Trigger words detected: {', '.join(trigger_words_list)}")
        else:
            reasons.append("No trigger words detected")
        
        return "; ".join(reasons)
    
    def get_soundscape_recommendation(self, text: str) -> Dict[str, Any]:
        """
        Gets a complete soundscape recommendation for a page.
        This is the main method to use for generating soundscapes.
        
        Args:
            text: Page content
            
        Returns:
            Dictionary with soundscape data ready for the frontend
        """
        analysis = self.analyze_page_complete(text)
        
        # Format trigger words for frontend
        formatted_triggers = []
        for trigger in analysis["trigger_words"]:
            formatted_triggers.append({
                "word": trigger["word"],
                "sound": trigger["sound"],
                "timing": trigger["timing"],
                "description": f"Trigger word '{trigger['word']}' at {trigger['timing']:.1f}s"
            })
        
        return {
            "carpet_tracks": [analysis["carpet_sound"]] if analysis["carpet_sound"] != "default_ambience" else [],
            "triggered_sounds": formatted_triggers,
            "mood": analysis["primary_mood"],
            "confidence": analysis["confidence"],
            "reasoning": analysis["reasoning"]
        }

def analyze_page_complete(text: str) -> Dict[str, Any]:
    """
    Convenience function for quick page analysis.
    
    Args:
        text: Page content to analyze
        
    Returns:
        Complete analysis dictionary
    """
    analyzer = PageAnalyzer()
    return analyzer.analyze_page_complete(text)

def get_soundscape_recommendation(text: str) -> Dict[str, Any]:
    """
    Convenience function for getting soundscape recommendations.
    
    Args:
        text: Page content to analyze
        
    Returns:
        Soundscape recommendation ready for frontend
    """
    analyzer = PageAnalyzer()
    return analyzer.get_soundscape_recommendation(text) 
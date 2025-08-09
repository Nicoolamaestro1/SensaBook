#!/usr/bin/env python3
"""
Test script for the massively enhanced mood analyzer with phrase recognition
"""

from app.services.mood_analyzer import AdvancedMoodAnalyzer
from app.services.page_analyzer import PageAnalyzer

def test_enhanced_mood_analyzer():
    """Test the massively enhanced mood analyzer"""
    
    print("🧪 Testing Massively Enhanced Mood Analyzer with Phrase Recognition")
    print("=" * 80)
    
    analyzer = AdvancedMoodAnalyzer()
    
    # Test texts with complex phrases and context
    test_texts = [
        {
            "name": "Peaceful Mountain Journey",
            "text": "The gentle breeze rustled through the alpine meadow as they walked along the mountain path. The summit view was breathtaking, and the peaceful silence was broken only by the soft whispers of the wind. It was a tranquil setting where they could find calm waters and serene beauty."
        },
        {
            "name": "Epic Battle Scene",
            "text": "The bridge of Khazad-dûm trembled as the Balrog approached with overwhelming force. Thunder crashed through the ancient halls, and lightning flashed as fire erupted from the demon's nostrils. The epic battle was fierce and terrifying, with tremendous power on display. The heroic struggle against the mighty force was overwhelming."
        },
        {
            "name": "Mystical Encounter",
            "text": "Galadriel's presence filled the air with an otherworldly aura. The ancient wisdom of the Eldar seemed to flow through the very stones of the chamber. Magical spells were cast, and ethereal light illuminated the sacred ground. The mystical energy was enchanting, and supernatural forces were at work."
        },
        {
            "name": "Romantic Evening",
            "text": "Their eyes met across the candlelit room, and love blossomed in their hearts. The romantic atmosphere was filled with passion and desire. Their hearts were beating fast as they shared a sweet kiss. The beloved presence created a perfect romantic evening where love was eternal."
        },
        {
            "name": "Dark and Dangerous Night",
            "text": "The dark presence of evil forces lurked in the shadows. Corruption was spreading through the ancient ruins, and death was approaching. The sinister plot was revealed as malicious intent became clear. The rotten atmosphere was filled with decay, and the dark magic was terrifying."
        },
        {
            "name": "Stormy Adventure",
            "text": "The storm was approaching with thunder crashing and lightning flashing. Rain was pouring down as they crossed the river in their boat. The tempest was raging around them, and the wind was howling through the mountain pass. It was a treacherous journey through dangerous terrain."
        },
        {
            "name": "Victory Celebration",
            "text": "Victory was achieved at last! The triumphant moment brought joyous celebration as hope was restored. The light was breaking through the darkness, and salvation was found. The victory march was accompanied by triumphant cheers and joyous laughter. The celebration feast was prepared with merry company."
        },
        {
            "name": "Mysterious Discovery",
            "text": "The mystery was deep and enigmatic. Puzzling clues were scattered throughout the ancient ruins. The curious case revealed cryptic messages with obscure meanings. Secret passages were hidden behind crumbling walls, and the strange atmosphere was filled with intrigue."
        },
        {
            "name": "Desperate Situation",
            "text": "The desperate situation required urgent action. It was a critical moment with emergency response needed. The last chance was approaching, and the final attempt was their only hope. The doomed effort seemed hopeless, but they had to try one more time."
        },
        {
            "name": "Ceremonial Ritual",
            "text": "The ceremony began with solemn atmosphere and dignified presence. The ritual was performed on sacred ground with reverent silence. The formal occasion was marked by official recognition and ancient traditions. The ceremony was complete with dignified ceremony and sacred moment."
        }
    ]
    
    for i, test_case in enumerate(test_texts, 1):
        print(f"\n📖 Test {i}: {test_case['name']}")
        print("-" * 60)
        
        try:
            # Test mood analysis
            mood_analysis = analyzer.analyze_page_mood(test_case['text'])
            
            print(f"✅ Enhanced Mood Analysis:")
            print(f"   Primary Mood: {mood_analysis.primary_mood}")
            print(f"   Secondary Mood: {mood_analysis.secondary_mood}")
            print(f"   Confidence: {mood_analysis.confidence:.3f}")
            print(f"   Suggested Sound: {mood_analysis.suggested_sound}")
            print(f"   Emotional Intensity: {mood_analysis.emotional_intensity:.3f}")
            print(f"   Atmospheric Density: {mood_analysis.atmospheric_density:.3f}")
            print(f"   Context Phrases: {mood_analysis.context_phrases[:3]}")
            print(f"   Reasoning: {mood_analysis.reasoning}")
            
            # Show detected elements
            print(f"   Detected Elements: {dict(list(mood_analysis.detected_elements.items())[:5])}")
            
        except Exception as e:
            print(f"❌ Error in mood analysis: {e}")
    
    print("\n" + "=" * 80)
    print("✅ Enhanced Mood Analyzer Test Complete!")

def test_enhanced_page_analyzer():
    """Test the enhanced page analyzer with the new mood analyzer"""
    
    print("\n🔬 Testing Enhanced Page Analyzer with Advanced Mood Analyzer")
    print("=" * 60)
    
    page_analyzer = PageAnalyzer()
    
    # Test complex text
    complex_text = """
    The epic battle raged on the bridge of Khazad-dûm as the Balrog approached with overwhelming force. 
    Thunder crashed through the ancient halls, and lightning flashed as fire erupted from the demon's nostrils. 
    The heroic struggle was fierce and terrifying, with tremendous power on display. 
    The mystical energy of the ancient realm was palpable, and the dark presence of evil forces lurked in the shadows.
    """
    
    try:
        # Test complete analysis
        analysis = page_analyzer.analyze_page_complete(complex_text)
        
        print(f"✅ Complete Page Analysis:")
        print(f"   Carpet Sound: {analysis['carpet_sound']}")
        print(f"   Primary Mood: {analysis['primary_mood']}")
        print(f"   Primary Emotion: {analysis['primary_emotion']}")
        print(f"   Primary Theme: {analysis['primary_theme']}")
        print(f"   Emotion Intensity: {analysis['emotion_intensity']:.3f}")
        print(f"   Atmosphere: {analysis['atmosphere']}")
        print(f"   Confidence: {analysis['confidence']:.3f}")
        print(f"   Trigger Words: {len(analysis['trigger_words'])}")
        print(f"   Context Phrases: {analysis['context_phrases'][:3]}")
        print(f"   Emotional Intensity: {analysis['emotional_intensity']:.3f}")
        print(f"   Atmospheric Density: {analysis['atmospheric_density']:.3f}")
        print(f"   Reasoning: {analysis['reasoning']}")
        
        # Test soundscape recommendation
        soundscape = page_analyzer.get_soundscape_recommendation(complex_text)
        print(f"\n   Soundscape Recommendation:")
        print(f"   Carpet Tracks: {soundscape['carpet_tracks']}")
        print(f"   Triggered Sounds: {len(soundscape['triggered_sounds'])}")
        print(f"   Mood: {soundscape['mood']}")
        print(f"   Emotion: {soundscape['emotion']}")
        print(f"   Theme: {soundscape['theme']}")
        
    except Exception as e:
        print(f"❌ Error in page analysis: {e}")

def test_phrase_recognition():
    """Test the sophisticated phrase recognition capabilities"""
    
    print("\n🎯 Testing Sophisticated Phrase Recognition")
    print("=" * 50)
    
    analyzer = AdvancedMoodAnalyzer()
    
    # Test specific phrases
    phrase_tests = [
        {
            "name": "Mountain Phrases",
            "text": "They reached the mountain peak and gazed at the cliff face. The ridge line stretched before them, and the summit view was magnificent. The alpine air was crisp and the high elevation made breathing difficult."
        },
        {
            "name": "Storm Phrases", 
            "text": "The storm was approaching with thunder crashing and lightning flashing. Rain was pouring down as the tempest raged around them. The gale force winds were howling through the valley."
        },
        {
            "name": "Romantic Phrases",
            "text": "Love was blooming between them as romance grew stronger. Their passion was burning bright and affection was shown in every gesture. The romantic moment was perfect as their hearts beat together."
        },
        {
            "name": "Mystical Phrases",
            "text": "The magical aura surrounded them as mystical power flowed through the ancient stones. Ethereal beauty was everywhere, and otherworldly presence filled the air. The enchanting melody of the sacred ritual was divine."
        }
    ]
    
    for test_case in phrase_tests:
        print(f"\n📝 {test_case['name']}:")
        
        try:
            analysis = analyzer.analyze_page_mood(test_case['text'])
            print(f"   Primary Mood: {analysis.primary_mood}")
            print(f"   Context Phrases: {analysis.context_phrases}")
            print(f"   Confidence: {analysis.confidence:.3f}")
            
        except Exception as e:
            print(f"   ❌ Error: {e}")

if __name__ == "__main__":
    test_enhanced_mood_analyzer()
    test_enhanced_page_analyzer()
    test_phrase_recognition() 
#!/usr/bin/env python3
"""
Test script for the regex-enhanced mood analyzer with complex pattern matching
"""

from app.services.mood_analyzer import AdvancedMoodAnalyzer
from app.services.page_analyzer import PageAnalyzer
import re

def test_regex_pattern_matching():
    """Test the sophisticated regex pattern matching capabilities"""
    
    print("🔍 Testing Regex-Enhanced Mood Analyzer with Complex Pattern Matching")
    print("=" * 80)
    
    analyzer = AdvancedMoodAnalyzer()
    
    # Test complex texts with specific regex patterns
    test_texts = [
        {
            "name": "Epic Battle with Regex Patterns",
            "text": "The epic battle raged across the battlefield as heroic warriors fought with tremendous power. The mighty force was overwhelming, and the grand scale of the conflict was magnificent. The powerful presence of the enemy was terrifying."
        },
        {
            "name": "Mystical Magic with Regex Patterns",
            "text": "The magical aura surrounded the ancient chamber as mystical power flowed through the stones. The ethereal beauty was enchanting, and the supernatural force was divine. The sacred ground was filled with ancient wisdom."
        },
        {
            "name": "Romantic Love with Regex Patterns",
            "text": "Love was blooming between them as romance grew stronger. Their passion was burning bright and affection was shown in every gesture. The romantic moment was perfect as their hearts beat together. The beloved presence created a sweet kiss."
        },
        {
            "name": "Dark Evil with Regex Patterns",
            "text": "The dark presence of evil forces lurked in the shadows. Corruption was spreading through the ancient ruins, and death was approaching. The sinister plot was revealed as malicious intent became clear. The rotten atmosphere was filled with decay."
        },
        {
            "name": "Storm Weather with Regex Patterns",
            "text": "The storm was approaching with thunder crashing and lightning flashing. Rain was pouring down as the tempest raged around them. The gale force winds were howling through the valley. The wind was blowing fiercely."
        },
        {
            "name": "Mountain Journey with Regex Patterns",
            "text": "They reached the mountain peak and gazed at the cliff face. The ridge line stretched before them, and the summit view was magnificent. The alpine air was crisp and the high elevation made breathing difficult. The long journey was challenging."
        },
        {
            "name": "Peaceful Calm with Regex Patterns",
            "text": "The peaceful silence was broken only by the gentle breeze. The tranquil atmosphere was serene and the calm waters reflected the soft light. The cozy atmosphere was comfortable and warm. The serene beauty was breathtaking."
        },
        {
            "name": "Victory Triumph with Regex Patterns",
            "text": "Victory was achieved at last! The triumphant moment brought joyous celebration as hope was restored. The light was breaking through the darkness, and salvation was found. The victory march was accompanied by triumphant cheers."
        },
        {
            "name": "Mystery Intrigue with Regex Patterns",
            "text": "The mystery was deep and enigmatic. Puzzling clues were scattered throughout the ancient ruins. The curious case revealed cryptic messages with obscure meanings. Secret passages were hidden behind crumbling walls."
        },
        {
            "name": "Danger Peril with Regex Patterns",
            "text": "Danger was lurking around every corner. Peril was ahead and the threat was growing stronger. The deadly force was lethal and the treacherous path was risky. The hazardous situation was real and dangerous."
        },
        {
            "name": "Desperation Urgency with Regex Patterns",
            "text": "The desperate situation required urgent action. It was a critical moment with emergency response needed. The last chance was approaching, and the final attempt was their only hope. The doomed effort seemed hopeless."
        },
        {
            "name": "Ceremony Ritual with Regex Patterns",
            "text": "The ceremony began with solemn atmosphere and dignified presence. The ritual was performed on sacred ground with reverent silence. The formal occasion was marked by official recognition and ancient traditions."
        }
    ]
    
    for i, test_case in enumerate(test_texts, 1):
        print(f"\n📖 Test {i}: {test_case['name']}")
        print("-" * 60)
        
        try:
            # Test mood analysis
            mood_analysis = analyzer.analyze_page_mood(test_case['text'])
            
            print(f"✅ Regex-Enhanced Mood Analysis:")
            print(f"   Primary Mood: {mood_analysis.primary_mood}")
            print(f"   Secondary Mood: {mood_analysis.secondary_mood}")
            print(f"   Confidence: {mood_analysis.confidence:.3f}")
            print(f"   Suggested Sound: {mood_analysis.suggested_sound}")
            print(f"   Emotional Intensity: {mood_analysis.emotional_intensity:.3f}")
            print(f"   Atmospheric Density: {mood_analysis.atmospheric_density:.3f}")
            print(f"   Context Phrases: {mood_analysis.context_phrases[:3]}")
            print(f"   Reasoning: {mood_analysis.reasoning}")
            
            # Show detected regex patterns
            if "epic_battle" in mood_analysis.detected_elements:
                print(f"   Epic Battle Pattern: {mood_analysis.detected_elements['epic_battle']}")
            if "mystical_magic" in mood_analysis.detected_elements:
                print(f"   Mystical Magic Pattern: {mood_analysis.detected_elements['mystical_magic']}")
            if "romantic_love" in mood_analysis.detected_elements:
                print(f"   Romantic Love Pattern: {mood_analysis.detected_elements['romantic_love']}")
            
        except Exception as e:
            print(f"❌ Error in mood analysis: {e}")
    
    print("\n" + "=" * 80)
    print("✅ Regex-Enhanced Mood Analyzer Test Complete!")

def test_regex_pattern_details():
    """Test specific regex patterns and their matching capabilities"""
    
    print("\n🎯 Testing Specific Regex Pattern Details")
    print("=" * 50)
    
    analyzer = AdvancedMoodAnalyzer()
    
    # Test specific regex patterns
    pattern_tests = [
        {
            "name": "Epic Battle Pattern",
            "text": "epic battle heroic struggle mighty force",
            "expected_pattern": "epic_battle"
        },
        {
            "name": "Mystical Magic Pattern",
            "text": "magical aura mystical power ethereal beauty",
            "expected_pattern": "mystical_magic"
        },
        {
            "name": "Romantic Love Pattern",
            "text": "love blooming passion burning heart beating",
            "expected_pattern": "romantic_love"
        },
        {
            "name": "Storm Weather Pattern",
            "text": "storm approaching thunder crashing rain pouring",
            "expected_pattern": "storm_weather"
        },
        {
            "name": "Mountain Journey Pattern",
            "text": "mountain peak cliff face alpine air",
            "expected_pattern": "mountain_journey"
        }
    ]
    
    for test_case in pattern_tests:
        print(f"\n📝 {test_case['name']}:")
        
        try:
            analysis = analyzer.analyze_page_mood(test_case['text'])
            print(f"   Primary Mood: {analysis.primary_mood}")
            print(f"   Expected Pattern: {test_case['expected_pattern']}")
            
            # Check if expected pattern was detected
            if test_case['expected_pattern'] in analysis.detected_elements:
                pattern_data = analysis.detected_elements[test_case['expected_pattern']]
                print(f"   Pattern Detected: ✅ (score: {pattern_data['score']})")
                print(f"   Matches: {pattern_data['matches'][:3]}")
            else:
                print(f"   Pattern Detected: ❌")
            
            print(f"   Confidence: {analysis.confidence:.3f}")
            
        except Exception as e:
            print(f"   ❌ Error: {e}")

def test_context_rules():
    """Test the context-based decision rules"""
    
    print("\n🌍 Testing Context-Based Decision Rules")
    print("=" * 50)
    
    analyzer = AdvancedMoodAnalyzer()
    
    # Test context rules
    context_tests = [
        {
            "name": "Geographic Override - Mountains",
            "text": "They climbed the mountain peak and reached the summit. The alpine air was crisp.",
            "expected_override": "geo_mountains"
        },
        {
            "name": "Geographic Override - Water",
            "text": "They crossed the river and sailed in their boat. The flowing water was clear.",
            "expected_override": "geo_water"
        },
        {
            "name": "Geographic Override - Indoors",
            "text": "Inside the room, the house was warm. The building had a cozy atmosphere.",
            "expected_override": "geo_indoors"
        },
        {
            "name": "Geographic Override - Night",
            "text": "The night was dark and the stars were shining. The moon was bright.",
            "expected_override": "geo_night"
        },
        {
            "name": "Intensity Modifier - High",
            "text": "The intense emotion was overwhelming. The powerful impact was strong.",
            "expected_modifier": "intensity_high_intensity"
        },
        {
            "name": "Intensity Modifier - Low",
            "text": "The gentle emotion was soft. The quiet feeling was calm.",
            "expected_modifier": "intensity_low_intensity"
        }
    ]
    
    for test_case in context_tests:
        print(f"\n🌍 {test_case['name']}:")
        
        try:
            analysis = analyzer.analyze_page_mood(test_case['text'])
            print(f"   Primary Mood: {analysis.primary_mood}")
            print(f"   Suggested Sound: {analysis.suggested_sound}")
            
            # Check for context rules
            context_detected = False
            for key in analysis.detected_elements.keys():
                if key.startswith("geo_") or key.startswith("intensity_"):
                    print(f"   Context Rule Detected: ✅ {key}")
                    context_detected = True
                    break
            
            if not context_detected:
                print(f"   Context Rule Detected: ❌")
            
            print(f"   Confidence: {analysis.confidence:.3f}")
            
        except Exception as e:
            print(f"   ❌ Error: {e}")

def test_complex_decision_making():
    """Test the complex decision-making logic"""
    
    print("\n🧠 Testing Complex Decision-Making Logic")
    print("=" * 50)
    
    analyzer = AdvancedMoodAnalyzer()
    
    # Test complex scenarios with multiple patterns
    complex_tests = [
        {
            "name": "Epic Battle + Mountain Context",
            "text": "The epic battle raged on the mountain peak. The heroic struggle was tremendous as they fought on the cliff face. The alpine air was filled with the sounds of war.",
            "expected_priority": "epic"  # Regex should take priority over geographic
        },
        {
            "name": "Romantic + Storm Context",
            "text": "Love was blooming between them as the storm approached. Their passion was burning bright while thunder crashed around them. The romantic moment was intense.",
            "expected_priority": "romantic"  # Regex should take priority over weather
        },
        {
            "name": "Mystical + Night Context",
            "text": "The magical aura surrounded them in the dark night. The mystical power flowed through the ancient chamber as the stars shone above. The ethereal beauty was enchanting.",
            "expected_priority": "mystical"  # Regex should take priority over night context
        },
        {
            "name": "Only Geographic Context",
            "text": "They walked through the mountain pass. The alpine meadow was beautiful. The high elevation made breathing difficult.",
            "expected_priority": "journey"  # Should use geographic override
        },
        {
            "name": "Only Traditional Keywords",
            "text": "The peaceful garden was calm and quiet. The gentle breeze was soft and the tranquil atmosphere was serene.",
            "expected_priority": "peaceful"  # Should use traditional analysis
        }
    ]
    
    for test_case in complex_tests:
        print(f"\n🧠 {test_case['name']}:")
        
        try:
            analysis = analyzer.analyze_page_mood(test_case['text'])
            print(f"   Primary Mood: {analysis.primary_mood}")
            print(f"   Expected Priority: {test_case['expected_priority']}")
            print(f"   Suggested Sound: {analysis.suggested_sound}")
            print(f"   Confidence: {analysis.confidence:.3f}")
            
            if analysis.primary_mood == test_case['expected_priority']:
                print(f"   Decision Correct: ✅")
            else:
                print(f"   Decision Correct: ❌ (got {analysis.primary_mood}, expected {test_case['expected_priority']})")
            
            print(f"   Reasoning: {analysis.reasoning}")
            
        except Exception as e:
            print(f"   ❌ Error: {e}")

def test_regex_performance():
    """Test regex performance with complex patterns"""
    
    print("\n⚡ Testing Regex Performance")
    print("=" * 40)
    
    analyzer = AdvancedMoodAnalyzer()
    
    # Test with complex text containing multiple patterns
    complex_text = """
    The epic battle raged on the mountain peak as the Balrog approached with overwhelming force. 
    Thunder crashed through the ancient halls, and lightning flashed as fire erupted from the demon's nostrils. 
    The magical aura surrounded the chamber as mystical power flowed through the very stones. 
    Love was blooming between the heroes as their passion burned bright in the face of danger. 
    The dark presence of evil forces lurked in the shadows while corruption spread through the ancient ruins. 
    The storm was approaching with thunder crashing and lightning flashing as rain poured down. 
    They reached the mountain peak and gazed at the cliff face while the alpine air was crisp. 
    The peaceful silence was broken only by the gentle breeze as the tranquil atmosphere was serene. 
    Victory was achieved at last as the triumphant moment brought joyous celebration. 
    The mystery was deep and enigmatic as puzzling clues were scattered throughout the ruins. 
    Danger was lurking around every corner as peril was ahead and the threat was growing stronger. 
    The desperate situation required urgent action as it was a critical moment with emergency response needed. 
    The ceremony began with solemn atmosphere and dignified presence as the ritual was performed on sacred ground.
    """
    
    try:
        print(f"📊 Analyzing complex text with {len(complex_text)} characters...")
        
        import time
        start_time = time.time()
        
        analysis = analyzer.analyze_page_mood(complex_text)
        
        end_time = time.time()
        processing_time = end_time - start_time
        
        print(f"✅ Analysis Complete:")
        print(f"   Processing Time: {processing_time:.4f} seconds")
        print(f"   Primary Mood: {analysis.primary_mood}")
        print(f"   Secondary Mood: {analysis.secondary_mood}")
        print(f"   Confidence: {analysis.confidence:.3f}")
        print(f"   Detected Patterns: {len([k for k in analysis.detected_elements.keys() if not k.startswith('geo_') and not k.startswith('intensity_')])}")
        print(f"   Context Rules: {len([k for k in analysis.detected_elements.keys() if k.startswith('geo_') or k.startswith('intensity_')])}")
        print(f"   Context Phrases: {len(analysis.context_phrases)}")
        print(f"   Reasoning: {analysis.reasoning}")
        
        # Show all detected patterns
        print(f"\n📋 All Detected Patterns:")
        for key, value in analysis.detected_elements.items():
            if isinstance(value, dict) and 'score' in value:
                print(f"   {key}: {value['mood']} (score: {value['score']})")
            else:
                print(f"   {key}: {value}")
        
    except Exception as e:
        print(f"❌ Error in performance test: {e}")

if __name__ == "__main__":
    test_regex_pattern_matching()
    test_regex_pattern_details()
    test_context_rules()
    test_complex_decision_making()
    test_regex_performance() 
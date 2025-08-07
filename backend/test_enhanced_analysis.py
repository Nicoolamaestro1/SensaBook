#!/usr/bin/env python3
"""
Test script for the enhanced analysis system with AdvancedEmotionAnalyzer
"""

from app.services.page_analyzer import analyze_page_complete, get_soundscape_recommendation
from app.services.emotion_analysis import AdvancedEmotionAnalyzer

def test_enhanced_analysis():
    """Test the enhanced analysis system"""
    
    print("🧪 Testing Enhanced Analysis with AdvancedEmotionAnalyzer")
    print("=" * 60)
    
    # Test texts with different emotional and thematic content
    test_texts = [
        {
            "name": "Peaceful Scene",
            "text": "The gentle breeze rustled through the leaves of the ancient oak trees. Frodo sat quietly by the stream, listening to the peaceful sounds of nature."
        },
        {
            "name": "Epic Battle Scene", 
            "text": "The bridge of Khazad-dûm trembled as the Balrog approached. Thunder echoed through the ancient halls, and fire erupted from the demon's nostrils. The battle was fierce and terrifying."
        },
        {
            "name": "Mystical Scene",
            "text": "Galadriel's presence filled the air with an otherworldly aura. The ancient wisdom of the Eldar seemed to flow through the very stones of the chamber. Magic and mystery surrounded them."
        },
        {
            "name": "Romantic Scene",
            "text": "Their eyes met across the candlelit room, and love blossomed in their hearts. The romantic atmosphere was filled with passion and desire."
        }
    ]
    
    for i, test_case in enumerate(test_texts, 1):
        print(f"\n📖 Test {i}: {test_case['name']}")
        print("-" * 40)
        
        try:
            # Test complete analysis
            analysis = analyze_page_complete(test_case['text'])
            
            print(f"✅ Analysis completed successfully")
            print(f"   Mood: {analysis['primary_mood']}")
            print(f"   Emotion: {analysis['primary_emotion']}")
            print(f"   Theme: {analysis['primary_theme']}")
            print(f"   Intensity: {analysis['emotion_intensity']:.2f}")
            print(f"   Atmosphere: {analysis['atmosphere']}")
            print(f"   Confidence: {analysis['confidence']:.2f}")
            print(f"   Carpet Sound: {analysis['carpet_sound']}")
            print(f"   Trigger Words: {len(analysis['trigger_words'])}")
            print(f"   Reasoning: {analysis['reasoning']}")
            
            # Test soundscape recommendations
            soundscape_recs = analysis.get('soundscape_recommendations', {})
            if soundscape_recs:
                print(f"   Soundscape Recs: {soundscape_recs.get('primary_soundscape', 'N/A')}")
            
        except Exception as e:
            print(f"❌ Error in analysis: {e}")
    
    print("\n" + "=" * 60)
    print("✅ Enhanced Analysis Test Complete!")

def test_advanced_emotion_analyzer():
    """Test the AdvancedEmotionAnalyzer directly"""
    
    print("\n🔬 Testing AdvancedEmotionAnalyzer Directly")
    print("=" * 40)
    
    analyzer = AdvancedEmotionAnalyzer()
    
    test_text = "The mountains were covered in snow and thunder echoed through the valley. Frodo felt fear in his heart as the storm approached."
    
    try:
        # Test emotion analysis
        emotion_result = analyzer.analyze_emotion(test_text)
        print(f"✅ Emotion Analysis:")
        print(f"   Primary Emotion: {emotion_result.primary_emotion.value}")
        print(f"   Intensity: {emotion_result.intensity:.2f}")
        print(f"   Confidence: {emotion_result.confidence:.2f}")
        print(f"   Keywords: {emotion_result.keywords}")
        
        # Test theme analysis
        theme_result = analyzer.analyze_theme(test_text)
        print(f"\n✅ Theme Analysis:")
        print(f"   Primary Theme: {theme_result.primary_theme.value}")
        print(f"   Atmosphere: {theme_result.atmosphere}")
        print(f"   Setting Elements: {theme_result.setting_elements}")
        
        # Test soundscape recommendations
        soundscape_recs = analyzer.generate_soundscape_recommendations(emotion_result, theme_result)
        print(f"\n✅ Soundscape Recommendations:")
        print(f"   Primary: {soundscape_recs['primary_soundscape']}")
        print(f"   Secondary: {soundscape_recs['secondary_soundscape']}")
        print(f"   Intensity: {soundscape_recs['intensity']:.2f}")
        print(f"   Volume: {soundscape_recs['recommended_volume']:.2f}")
        print(f"   Effects: {soundscape_recs['sound_effects']}")
        
    except Exception as e:
        print(f"❌ Error in AdvancedEmotionAnalyzer: {e}")

if __name__ == "__main__":
    test_enhanced_analysis()
    test_advanced_emotion_analyzer() 
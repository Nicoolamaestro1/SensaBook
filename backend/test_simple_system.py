#!/usr/bin/env python3
"""
Test Simple Soundscape System
Tests the new simplified, config-driven system
"""

from app.services.simple_scene_classifier import simple_scene_classifier
from app.services.simple_smart_soundscape import simple_smart_soundscape_service

def test_simple_system():
    """Test the simplified soundscape system."""
    
    print("🧹 Testing Simplified Soundscape System")
    print("=" * 50)
    print("Now with config files and clean architecture!")
    print("=" * 50)
    
    # Test the Dracula problem
    test_text = "They sat in the hotel dining room discussing the case. The castle was mentioned in passing."
    
    print(f"\n📖 Test Text: {test_text}")
    print("-" * 50)
    
    # Test scene classification
    print("🎭 Scene Classification:")
    scene_analysis = simple_scene_classifier.classify_scene(test_text, genre="mystery")
    print(f"  Primary Scene: {scene_analysis.primary_scene.value}")
    print(f"  Context: {scene_analysis.scene_context.value}")
    print(f"  Mood: {scene_analysis.mood}")
    print(f"  Intensity: {scene_analysis.intensity:.2f}")
    print(f"  Confidence: {scene_analysis.confidence:.2f}")
    print(f"  Audio Priority: {scene_analysis.audio_priority}")
    print(f"  Reasoning: {scene_analysis.reasoning}")
    print(f"  Genre Adjustments: {scene_analysis.genre_adjustments}")
    
    # Test soundscape generation
    print("\n🎵 Soundscape Generation:")
    soundscape = simple_smart_soundscape_service.generate_smart_soundscape(
        text=test_text, 
        genre="mystery"
    )
    print(f"  Primary Audio: {soundscape['primary_audio']}")
    print(f"  Secondary Audio: {soundscape['secondary_audio']}")
    print(f"  Scene Type: {soundscape['scene_type']}")
    print(f"  Genre: {soundscape['genre']}")
    
    # Test text analysis
    print("\n🔍 Text Analysis:")
    analysis = simple_smart_soundscape_service.analyze_text_scene(test_text, genre="mystery")
    print(f"  Explanation: {analysis['explanation']}")
    print(f"  Genre Intelligence: {analysis['genre_intelligence']}")
    
    print("\n" + "=" * 50)
    print("✅ Test completed successfully!")
    print("🎯 The Dracula problem should now be solved!")
    print("=" * 50)

if __name__ == "__main__":
    test_simple_system()


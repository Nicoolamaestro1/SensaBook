#!/usr/bin/env python3
"""
Test Smart Scene Classification System
Verifies that the advanced context-aware scene detection is working correctly
"""

from app.services.smart_scene_classifier import smart_scene_classifier

def test_smart_scene_classification():
    print("🧠 Testing Smart Scene Classification System")
    print("=" * 60)
    print("Verifying advanced context awareness and intelligent audio mapping")
    print()
    
    # Test 1: Hotel dining scene (should prioritize dining over castle)
    test_text_1 = "They sat in the elegant hotel dining room, discussing the case over fine wine. The castle was mentioned in passing, but the atmosphere was warm and intimate."
    
    print("📖 Test 1: Hotel Dining Scene")
    print(f"Text: {test_text_1}")
    print("-" * 50)
    
    analysis_1 = smart_scene_classifier.classify_scene(test_text_1, "mystery")
    
    print("🎭 Scene Analysis:")
    print(f"  Primary Scene: {analysis_1.primary_scene.value}")
    print(f"  Context: {analysis_1.scene_context.value}")
    print(f"  Mood: {analysis_1.mood}")
    print(f"  Intensity: {analysis_1.intensity:.2f}")
    print(f"  Confidence: {analysis_1.confidence:.2f}")
    print(f"  Audio Priority: {analysis_1.audio_priority}")
    print(f"  Emotional Arc: {analysis_1.emotional_arc}")
    print(f"  Atmospheric Qualities: {', '.join(analysis_1.atmospheric_qualities)}")
    print(f"  Sound Layers: {', '.join(analysis_1.sound_layers)}")
    print(f"  Ambient Suggestions: {', '.join(analysis_1.ambient_suggestions)}")
    print()
    
    print("🔍 Reasoning:")
    print(f"  {analysis_1.reasoning}")
    print()
    
    print("🎵 Audio Mapping:")
    print(f"  Primary: {analysis_1.audio_priority}")
    print(f"  Layers: {', '.join(analysis_1.sound_layers)}")
    print(f"  Ambient: {', '.join(analysis_1.ambient_suggestions)}")
    print()
    
    # Test 2: Stormy castle scene
    test_text_2 = "The storm raged outside the ancient castle walls. Thunder boomed and lightning illuminated the dark corridors. Footsteps echoed through the eerie silence."
    
    print("📖 Test 2: Stormy Castle Scene")
    print(f"Text: {test_text_2}")
    print("-" * 50)
    
    analysis_2 = smart_scene_classifier.classify_scene(test_text_2, "horror")
    
    print("🎭 Scene Analysis:")
    print(f"  Primary Scene: {analysis_2.primary_scene.value}")
    print(f"  Context: {analysis_2.scene_context.value}")
    print(f"  Mood: {analysis_2.mood}")
    print(f"  Intensity: {analysis_2.intensity:.2f}")
    print(f"  Confidence: {analysis_2.confidence:.2f}")
    print(f"  Audio Priority: {analysis_2.audio_priority}")
    print(f"  Emotional Arc: {analysis_2.emotional_arc}")
    print(f"  Atmospheric Qualities: {', '.join(analysis_2.atmospheric_qualities)}")
    print(f"  Sound Layers: {', '.join(analysis_2.sound_layers)}")
    print(f"  Ambient Suggestions: {', '.join(analysis_2.ambient_suggestions)}")
    print()
    
    print("🔍 Reasoning:")
    print(f"  {analysis_2.reasoning}")
    print()
    
    print("🎵 Audio Mapping:")
    print(f"  Primary: {analysis_2.audio_priority}")
    print(f"  Layers: {', '.join(analysis_2.sound_layers)}")
    print(f"  Ambient: {', '.join(analysis_2.ambient_suggestions)}")
    print()
    
    # Test 3: Intimate dialogue scene
    test_text_3 = "She whispered softly, 'I love you,' and he gently caressed her cheek. The candlelight flickered in the intimate darkness of their private chamber."
    
    print("📖 Test 3: Intimate Dialogue Scene")
    print(f"Text: {test_text_3}")
    print("-" * 50)
    
    analysis_3 = smart_scene_classifier.classify_scene(test_text_3, "romance")
    
    print("🎭 Scene Analysis:")
    print(f"  Primary Scene: {analysis_3.primary_scene.value}")
    print(f"  Context: {analysis_3.scene_context.value}")
    print(f"  Mood: {analysis_3.mood}")
    print(f"  Intensity: {analysis_3.intensity:.2f}")
    print(f"  Confidence: {analysis_3.confidence:.2f}")
    print(f"  Audio Priority: {analysis_3.audio_priority}")
    print(f"  Emotional Arc: {analysis_3.emotional_arc}")
    print(f"  Atmospheric Qualities: {', '.join(analysis_3.atmospheric_qualities)}")
    print(f"  Sound Layers: {', '.join(analysis_3.sound_layers)}")
    print(f"  Ambient Suggestions: {', '.join(analysis_3.ambient_suggestions)}")
    print()
    
    print("🔍 Reasoning:")
    print(f"  {analysis_3.reasoning}")
    print()
    
    print("🎵 Audio Mapping:")
    print(f"  Primary: {analysis_3.audio_priority}")
    print(f"  Layers: {', '.join(analysis_3.sound_layers)}")
    print(f"  Ambient: {', '.join(analysis_3.ambient_suggestions)}")
    print()
    
    print("=" * 60)
    
    # Validation checks
    success = True
    issues = []
    
    # Check if Test 1 correctly identifies hotel dining
    if "hotel" not in analysis_1.audio_priority.lower() and "dining" not in analysis_1.audio_priority.lower():
        success = False
        issues.append("Test 1: Failed to prioritize hotel dining over castle")
    
    # Check if Test 2 correctly identifies stormy atmosphere
    if "storm" not in analysis_2.audio_priority.lower() and "stormy" not in str(analysis_2.atmospheric_qualities):
        success = False
        issues.append("Test 2: Failed to detect stormy atmosphere")
    
    # Check if Test 3 correctly identifies intimate dialogue
    if "intimate" not in analysis_3.audio_priority.lower() and "intimate" not in str(analysis_3.atmospheric_qualities):
        success = False
        issues.append("Test 3: Failed to detect intimate atmosphere")
    
    # Check if atmospheric qualities are being detected
    if not analysis_1.atmospheric_qualities and not analysis_2.atmospheric_qualities and not analysis_3.atmospheric_qualities:
        success = False
        issues.append("No atmospheric qualities detected in any test")
    
    if success:
        print("✅ All smart scene classification tests passed!")
        print("🎯 The system now provides:")
        print("   • Advanced context awareness")
        print("   • Intelligent audio mapping")
        print("   • Atmospheric quality detection")
        print("   • Emotional arc recognition")
        print("   • Sophisticated scene understanding")
    else:
        print("❌ Issues found:")
        for issue in issues:
            print(f"   • {issue}")
    
    print("=" * 60)
    return success

if __name__ == "__main__":
    test_smart_scene_classification()

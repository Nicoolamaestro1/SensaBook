#!/usr/bin/env python3
"""
Test the complex scene detection system
This shows you how the regex patterns and psychoacoustic analysis work
"""

from app.services.soundscape import enhanced_scene_detection, get_ambient_soundscape
from app.services.emotion_analysis import find_trigger_words

def test_complex_scene_detection():
    """Test the complex scene detection with different types of text"""
    
    print("🎭 Testing Complex Scene Detection System")
    print("=" * 60)
    
    # Test 1: Epic Battle Scene
    print("\n🔥 TEST 1: Epic Battle Scene")
    battle_text = "The epic battle raged across the battlefield. Warriors clashed with tremendous force, their hearts racing with adrenaline. The ultimate confrontation was at hand."
    
    print(f"Text: '{battle_text}'")
    print()
    
    # Get scene detection
    scenes, counts, positions, mood_analysis = enhanced_scene_detection(battle_text)
    
    print("🎯 Detected Scenes:")
    for scene in scenes[:3]:  # Show top 3
        print(f"  • {scene}")
    
    print(f"\n📊 Scene Counts: {counts}")
    
    if mood_analysis:
        print(f"\n🎵 Mood Analysis:")
        for scene, data in list(mood_analysis.items())[:3]:
            print(f"  • {scene}: {data.get('mood', 'unknown')} mood")
    
    # Test 2: Romantic Scene
    print("\n" + "=" * 60)
    print("\n💕 TEST 2: Romantic Scene")
    romantic_text = "Their love was blooming with genuine affection. The romantic evening created a cherished moment of deep connection. Their hearts beat as one in this intimate atmosphere."
    
    print(f"Text: '{romantic_text}'")
    print()
    
    scenes2, counts2, positions2, mood_analysis2 = enhanced_scene_detection(romantic_text)
    
    print("🎯 Detected Scenes:")
    for scene in scenes2[:3]:
        print(f"  • {scene}")
    
    print(f"\n📊 Scene Counts: {counts2}")
    
    # Test 3: Mystical Scene
    print("\n" + "=" * 60)
    print("\n✨ TEST 3: Mystical Scene")
    mystical_text = "Ancient wisdom flowed through the enchanted realm. Magical energy radiated from the mystical presence. The ethereal atmosphere shimmered with otherworldly beauty."
    
    print(f"Text: '{mystical_text}'")
    print()
    
    scenes3, counts3, positions3, mood_analysis3 = enhanced_scene_detection(mystical_text)
    
    print("🎯 Detected Scenes:")
    for scene in scenes3[:3]:
        print(f"  • {scene}")
    
    print(f"\n📊 Scene Counts: {counts3}")
    
    # Test 4: Compare Simple vs Complex
    print("\n" + "=" * 60)
    print("\n🔍 COMPARISON: Simple Triggers vs Complex Scenes")
    
    mixed_text = "The wind howled as an epic battle began. Thunder crashed overhead while magical energy flowed through the ancient castle."
    
    print(f"Text: '{mixed_text}'")
    print()
    
    # Simple triggers
    print("🎵 Simple Triggers (Layer 1):")
    triggers = find_trigger_words(mixed_text)
    for trigger in triggers:
        print(f"  • '{trigger['word']}' → {trigger['sound']}")
    
    # Complex scenes
    print("\n🎭 Complex Scenes (Layer 2):")
    scenes4, counts4, positions4, mood_analysis4 = enhanced_scene_detection(mixed_text)
    for scene in scenes4[:3]:
        print(f"  • {scene}")
    
    print(f"\n📊 Scene Counts: {counts4}")

def test_psychoacoustic_metadata():
    """Test the psychoacoustic metadata system"""
    
    print("\n" + "=" * 60)
    print("\n🧠 TESTING PSYCHOACOUSTIC METADATA")
    
    # Look at the actual metadata from the system
    from app.services.soundscape import ENHANCED_SCENE_SOUND_MAPPINGS
    
    print("\n🎵 Available Scene Types and Their Audio Characteristics:")
    
    for scene_type, scene_data in list(ENHANCED_SCENE_SOUND_MAPPINGS.items())[:5]:
        print(f"\n🎭 {scene_type.upper()}:")
        print(f"  Mood: {scene_data.get('mood', 'unknown')}")
        print(f"  Weight: {scene_data.get('weight', 'unknown')}")
        print(f"  Background: {scene_data.get('carpet', 'none')}")
        
        if 'psychoacoustic' in scene_data:
            psycho = scene_data['psychoacoustic']
            print(f"  🎧 Audio Profile:")
            print(f"    • Frequency: {psycho.get('frequency_range', 'unknown')}")
            print(f"    • Stereo Width: {psycho.get('spatial_width', 'unknown')}")
            print(f"    • Dynamics: {psycho.get('temporal_dynamics', 'unknown')}")
            print(f"    • Reverb: {psycho.get('reverb_type', 'unknown')}")

if __name__ == "__main__":
    test_complex_scene_detection()
    test_psychoacoustic_metadata()
    
    print("\n" + "=" * 60)
    print("\n💡 SUMMARY:")
    print("• Layer 1 (Simple): Finds individual words → plays sounds")
    print("• Layer 2 (Complex): Finds scene patterns → sets mood + background")
    print("• Layer 3 (Advanced): Optimizes audio mix for best experience")
    print("\n🎯 The complex system makes the simple system sound better!")

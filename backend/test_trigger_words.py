#!/usr/bin/env python3
"""
Test Trigger Words Functionality
Verifies that the simplified system can detect trigger words and return proper soundscape data
"""

from app.services.simple_smart_soundscape import simple_smart_soundscape_service

def test_trigger_words():
    print("🧪 Testing Trigger Words Functionality")
    print("=" * 50)
    print("Verifying that trigger words are detected and soundscape includes all required fields")
    print()
    
    # Test text with trigger words
    test_text = "The storm raged outside while footsteps echoed in the castle. Thunder boomed and wind howled through the corridors."
    
    print(f"📖 Test Text: {test_text}")
    print("-" * 50)
    
    # Generate soundscape
    soundscape = simple_smart_soundscape_service.generate_smart_soundscape(
        text=test_text,
        genre="horror"
    )
    
    print("🎭 Scene Analysis:")
    print(f"  Primary Scene: {soundscape.get('scene_type', 'N/A')}")
    print(f"  Context: {soundscape.get('scene_context', 'N/A')}")
    print(f"  Mood: {soundscape.get('mood', 'N/A')}")
    print(f"  Intensity: {soundscape.get('intensity', 'N/A')}")
    print(f"  Confidence: {soundscape.get('confidence', 'N/A')}")
    print(f"  Audio Priority: {soundscape.get('audio_priority', 'N/A')}")
    print()
    
    print("🎵 Audio Components:")
    print(f"  Primary Audio: {soundscape.get('primary_audio', 'N/A')}")
    print(f"  Secondary Audio: {soundscape.get('secondary_audio', 'N/A')}")
    print(f"  Carpet Tracks: {soundscape.get('carpet_tracks', [])}")
    print()
    
    print("🔊 Trigger Words Detected:")
    triggered_sounds = soundscape.get('triggered_sounds', [])
    if triggered_sounds:
        for trigger in triggered_sounds:
            print(f"  • '{trigger['word']}' at position {trigger['position']} → {trigger['file']}")
    else:
        print("  ❌ No trigger words detected!")
    print()
    
    print("📱 Mobile App Response Format:")
    # Simulate what the API would return
    mobile_response = {
        "book_id": soundscape.get("book_id"),
        "book_page_id": "test_1_1",
        "summary": soundscape.get("reasoning", "Scene analyzed successfully"),
        "detected_scenes": [soundscape.get("scene_type", "unknown")],
        "scene_keyword_counts": {soundscape.get("scene_type", "unknown"): 1},
        "scene_keyword_positions": {soundscape.get("scene_type", "unknown"): [0]},
        "carpet_tracks": soundscape.get("carpet_tracks", []),
        "triggered_sounds": soundscape.get("triggered_sounds", [])
    }
    
    for key, value in mobile_response.items():
        print(f"  {key}: {value}")
    
    print()
    print("=" * 50)
    
    # Validation checks
    success = True
    issues = []
    
    if not triggered_sounds:
        success = False
        issues.append("No trigger words detected")
    
    if not soundscape.get('carpet_tracks'):
        success = False
        issues.append("No carpet tracks generated")
    
    if not soundscape.get('primary_audio'):
        success = False
        issues.append("No primary audio specified")
    
    if success:
        print("✅ All trigger words functionality working correctly!")
        print("🎯 The mobile app should now receive proper soundscape data with:")
        print("   • Trigger words for sound effects")
        print("   • Carpet tracks for ambient background")
        print("   • Scene analysis and reasoning")
    else:
        print("❌ Issues found:")
        for issue in issues:
            print(f"   • {issue}")
    
    print("=" * 50)
    return success

if __name__ == "__main__":
    test_trigger_words()

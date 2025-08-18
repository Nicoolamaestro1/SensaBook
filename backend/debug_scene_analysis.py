#!/usr/bin/env python3
"""
Debug Scene Analysis
See exactly what's happening in the scene classification process
"""

from app.services.smart_scene_classifier import smart_scene_classifier

def debug_scene_analysis():
    print("🔍 Debugging Scene Analysis")
    print("=" * 50)
    
    # Test text
    test_text = "They sat in the elegant hotel dining room, discussing the case over fine wine. The castle was mentioned in passing, but the atmosphere was warm and intimate."
    
    print(f"📖 Test Text: {test_text}")
    print("-" * 50)
    
    # Debug the scene analysis step by step
    print("🔧 Debugging Scene Type Analysis:")
    
    # Check what patterns are loaded
    print(f"Scene patterns loaded: {list(smart_scene_classifier.scene_patterns.keys())}")
    
    # Test individual pattern matching
    for scene_name, config in smart_scene_classifier.scene_patterns.items():
        print(f"\n🎭 Testing {scene_name}:")
        print(f"  Base weight: {config['base_weight']}")
        print(f"  Patterns: {config['patterns']}")
        
        total_score = 0.0
        for pattern in config["patterns"]:
            import re
            matches = re.findall(pattern, test_text, re.IGNORECASE)
            if matches:
                print(f"    Pattern '{pattern}' found {len(matches)} matches: {matches}")
                total_score += len(matches) * config["base_weight"]
            else:
                print(f"    Pattern '{pattern}' - no matches")
        
        print(f"  Total score: {total_score}")
    
    print("\n" + "=" * 50)
    
    # Now test the full classification
    print("🎯 Full Scene Classification:")
    analysis = smart_scene_classifier.classify_scene(test_text, "mystery")
    
    print(f"Primary Scene: {analysis.primary_scene.value}")
    print(f"Audio Priority: {analysis.audio_priority}")
    print(f"Atmospheric Qualities: {analysis.atmospheric_qualities}")
    print(f"Sound Layers: {analysis.sound_layers}")
    print(f"Ambient Suggestions: {analysis.ambient_suggestions}")

if __name__ == "__main__":
    debug_scene_analysis()

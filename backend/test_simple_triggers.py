#!/usr/bin/env python3
"""
Simple test of the basic trigger word system
This shows you the EASY part that actually works!
"""

from app.services.emotion_analysis import find_trigger_words

def test_simple_triggers():
    """Test the simple trigger word detection"""
    
    # Test text with obvious trigger words
    test_text = "The wind howled through the trees as footsteps approached. A sword clashed against armor."
    
    print("🔍 Testing trigger word detection...")
    print(f"Text: '{test_text}'")
    print()
    
    # Find trigger words
    triggers = find_trigger_words(test_text)
    
    if triggers:
        print("✅ Found trigger words:")
        for trigger in triggers:
            print(f"  • '{trigger['word']}' → {trigger['sound']}")
            print(f"    Position: word {trigger['word_position']} of {trigger['word_count']}")
            print(f"    Timing: {trigger['timing']:.1f}s")
            print()
    else:
        print("❌ No trigger words found")
    
    print("=" * 50)
    
    # Test with different text
    test_text2 = "Rain fell softly on the castle walls. Thunder rumbled in the distance."
    print(f"Text 2: '{test_text2}'")
    print()
    
    triggers2 = find_trigger_words(test_text2)
    
    if triggers2:
        print("✅ Found trigger words:")
        for trigger in triggers2:
            print(f"  • '{trigger['word']}' → {trigger['sound']}")
            print(f"    Position: word {trigger['word_position']} of {trigger['word_count']}")
            print(f"    Timing: {trigger['timing']:.1f}s")
            print()
    else:
        print("❌ No trigger words found")

if __name__ == "__main__":
    test_simple_triggers()

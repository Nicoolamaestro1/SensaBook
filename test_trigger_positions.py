#!/usr/bin/env python3
"""
Test script for enhanced trigger word positioning functionality.
Tests the new position tracking features for frontend synchronization.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.emotion_analysis import find_trigger_words
from app.services.soundscape import _extract_trigger_positions

def test_trigger_word_positions():
    """Test trigger word detection with position information."""
    
    # Test text with various trigger words
    test_text = """
    The sword clashed against armor as thunder roared overhead. 
    Footsteps echoed through the castle corridors, and the sound of 
    a door creaking open filled the air. Fire crackled in the 
    fireplace, while water dripped from the ceiling.
    """
    
    print("🔍 Testing Enhanced Trigger Word Positioning")
    print("=" * 50)
    print(f"Test Text: {test_text.strip()}")
    print()
    
    # Get trigger words with positions
    trigger_words = find_trigger_words(test_text)
    
    print("📊 Trigger Words Found:")
    print("-" * 30)
    for i, trigger in enumerate(trigger_words):
        print(f"{i+1}. Word: '{trigger['word']}'")
        print(f"   Sound: {trigger['sound']}")
        print(f"   Character Position: {trigger['position']}")
        print(f"   Word Position: {trigger['word_position']}")
        print(f"   Timing: {trigger['timing']:.2f}s")
        print(f"   Context: {trigger.get('context', 'N/A')}")
        print()
    
    # Test position extraction
    print("🎯 Trigger Positions Organized:")
    print("-" * 30)
    positions = _extract_trigger_positions(trigger_words, test_text)
    
    for trigger_type, type_triggers in positions.items():
        print(f"\nType: {trigger_type}")
        print(f"Count: {len(type_triggers)}")
        
        for trigger in type_triggers:
            print(f"  • '{trigger['word']}' at word {trigger['word_position']} "
                  f"(char {trigger['character_position']}) → {trigger['sound']}")
    
    print("\n✅ Enhanced trigger positioning test completed!")

def test_reading_synchronization():
    """Test how trigger words align with reading progression."""
    
    test_text = """
    The hero drew his sword. Lightning flashed across the sky. 
    Thunder boomed loudly. The castle gates creaked open. 
    Footsteps echoed in the distance. A fire burned brightly.
    """
    
    print("\n📖 Testing Reading Synchronization")
    print("=" * 40)
    
    trigger_words = find_trigger_words(test_text)
    
    # Simulate reading progression
    words = test_text.split()
    print(f"Total words: {len(words)}")
    print(f"Estimated reading time: {len(words) / 200.0 * 60:.1f} seconds")
    print()
    
    print("Reading progression with sound triggers:")
    print("-" * 40)
    
    for i, word in enumerate(words):
        # Check if this word position has a trigger
        triggers_at_position = [t for t in trigger_words if t['word_position'] == i]
        
        if triggers_at_position:
            for trigger in triggers_at_position:
                print(f"Word {i:2d}: '{word}' → 🔊 {trigger['sound']} "
                      f"(at {trigger['timing']:.1f}s)")
        else:
            print(f"Word {i:2d}: '{word}'")
    
    print("\n✅ Reading synchronization test completed!")

if __name__ == "__main__":
    try:
        test_trigger_word_positions()
        test_reading_synchronization()
        print("\n🎉 All tests passed successfully!")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()

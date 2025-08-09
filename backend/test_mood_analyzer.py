"""
Test script for the MoodAnalyzer service.
Demonstrates how the algorithm analyzes text and suggests appropriate sounds.
"""

from app.services.mood_analyzer import MoodAnalyzer, analyze_book_pages

def test_mood_analyzer():
    """Test the mood analyzer with sample text from The Lord of the Rings"""
    
    # Sample text from different parts of LOTR
    sample_texts = [
        # Peaceful Shire scene
        """The sun was already westering as they rode from Edoras, and the light of it was in their eyes, 
        turning all the rolling fields of Rohan to a golden haze. There was a beaten way, north-westward 
        along the foot-hills of the White Mountains, and this they followed, up and down in a green country, 
        crossing small swift streams by many fords. Far ahead and to their right the Misty Mountains loomed; 
        ever darker and taller they grew as the miles went by.""",
        
        # Tense/Epic scene
        """The bridge of Khazad-dûm was narrow, made of stone, and without parapet. It spanned the chasm 
        in a single arch. The Balrog reached the bridge. Gandalf stood in the middle of the span, leaning 
        on the staff in his left hand, but in his other hand Glamdring gleamed, cold and white. His enemy 
        halted again, facing him, and the shadow about it reached out like two vast wings. It raised the whip, 
        and the thongs whined and cracked. Fire came from its nostrils. But Gandalf stood firm.""",
        
        # Mystical scene
        """The Lady Galadriel was tall beyond the measure even of the women of the Noldor; she was strong 
        of body, mind, and will, a match for both the loremasters and the athletes of the Eldar in the days 
        of their youth. Even among the Eldar she was accounted beautiful, and her hair was held a marvel 
        unmatched. It was golden like the hair of her father and of her foremother Indis, but richer and 
        more radiant, for its gold was touched by some memory of the starlike silver of her mother; and the 
        Eldar said that the light of the Two Trees, Laurelin and Telperion, had been snared in her tresses.""",
        
        # Dark/Corrupt scene
        """The Ring was trying to get back to its master. It had slipped from Frodo's finger and would 
        betray him; for at once it took a new shape, and it fell upon his hand, and it was a ring of gold, 
        round and unadorned, the plain band of gold. But the writing upon it, which at first was as clear 
        as red flame, faded and was now only barely to be read. It was hot to the touch. Frodo felt a 
        sudden desire to put it on; and he had a feeling that if he did so, he would be able to see things 
        that were hidden from him.""",
        
        # Triumphant scene
        """The Eagles are coming! The Eagles are coming!' For at that moment there came a sound like 
        wind, but not the sound of wind. It was a sound like the wind in the leaves of trees, and the 
        sound of water, and the sound of birds singing. But it was none of these, for it was the sound 
        of the Eagles, and it was the sound of the Eagles that was the most beautiful sound that had ever 
        been heard in all the world."""
    ]
    
    analyzer = MoodAnalyzer()
    
    print("🧠 Testing Mood Analysis Algorithm")
    print("=" * 50)
    
    for i, text in enumerate(sample_texts, 1):
        print(f"\n📖 Sample Text {i}:")
        print("-" * 30)
        print(text[:200] + "..." if len(text) > 200 else text)
        
        # Analyze the text
        analysis = analyzer.analyze_page_mood(text)
        
        print(f"\n🎯 Analysis Results:")
        print(f"Primary Mood: {analysis.primary_mood}")
        print(f"Secondary Mood: {analysis.secondary_mood}")
        print(f"Confidence: {analysis.confidence:.2f}")
        print(f"Suggested Sound: {analysis.suggested_sound}")
        print(f"Reasoning: {analysis.reasoning}")
        
        print(f"\n📊 Detected Elements:")
        for element_type, elements in analysis.detected_elements.items():
            if elements:
                print(f"  {element_type}: {elements}")
    
    print("\n" + "=" * 50)
    print("✅ Mood Analysis Test Complete!")

def test_algorithm_explanation():
    """Explain how the algorithm works"""
    
    print("\n🔍 How the Mood Analysis Algorithm Works:")
    print("=" * 50)
    
    print("""
1. TEXT PREPROCESSING:
   - Convert text to lowercase
   - Remove punctuation (optional)
   - Split into words or phrases

2. KEYWORD DETECTION:
   - Scan for mood category keywords (peaceful, tense, epic, etc.)
   - Count geographic elements (mountains, forest, water, etc.)
   - Identify weather conditions (storm, night, wind, etc.)
   - Measure emotional intensity indicators

3. MOOD CLASSIFICATION:
   - Score each mood category based on keyword frequency
   - Consider geographic and weather context
   - Determine primary and secondary moods
   - Adjust based on emotional intensity

4. SOUND SUGGESTION:
   - Match primary mood to available sounds
   - Consider geographic/weather context for specific sounds
   - Fall back to secondary mood or default

5. CONFIDENCE CALCULATION:
   - Based on number of detected elements
   - Higher confidence with more strong indicators
   - Boost confidence for clear mood signals
    """)
    
    print("🎯 Algorithm Features:")
    print("- Context-aware analysis (geographic + weather + emotion)")
    print("- Confidence scoring for reliability")
    print("- Detailed reasoning for transparency")
    print("- Extensible keyword dictionaries")
    print("- Genre-specific mood categories")

if __name__ == "__main__":
    test_mood_analyzer()
    test_algorithm_explanation() 
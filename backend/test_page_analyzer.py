"""
Test script for the complete PageAnalyzer service.
Demonstrates how both mood analysis and emotion analysis work together.
"""

from app.services.page_analyzer import PageAnalyzer, analyze_page_complete, get_soundscape_recommendation

def test_complete_page_analysis():
    """Test the complete page analyzer with sample text"""
    
    # Sample text with both mood and trigger words
    sample_texts = [
        # Peaceful scene with wind trigger
        """The gentle breeze rustled through the leaves of the ancient oak trees. 
        Frodo sat quietly by the stream, listening to the peaceful sounds of nature. 
        The wind carried the sweet scent of wildflowers from the nearby meadow. 
        It was a perfect afternoon in the Shire, with nothing to disturb the tranquility.""",
        
        # Epic battle scene with multiple triggers
        """The bridge of Khazad-dûm trembled as the Balrog approached. 
        Thunder echoed through the ancient halls, and fire erupted from the demon's nostrils. 
        Gandalf stood firm, his staff glowing with white light. The wind howled through 
        the chasm as the two powerful beings prepared for their fateful confrontation.""",
        
        # Mystical scene with subtle triggers
        """Galadriel's presence filled the air with an otherworldly aura. 
        The ancient wisdom of the Eldar seemed to flow through the very stones of 
        Lothlórien. Her golden hair shimmered like starlight, and her eyes held 
        the depth of countless ages. The wind whispered secrets of the past."""
    ]
    
    analyzer = PageAnalyzer()
    
    print("🧠 Testing Complete Page Analysis")
    print("=" * 60)
    
    for i, text in enumerate(sample_texts, 1):
        print(f"\n📖 Sample Text {i}:")
        print("-" * 40)
        print(text[:150] + "..." if len(text) > 150 else text)
        
        # Get complete analysis
        analysis = analyzer.analyze_page_complete(text)
        
        print(f"\n🎯 Complete Analysis Results:")
        print(f"Primary Mood: {analysis['primary_mood']}")
        print(f"Secondary Mood: {analysis['secondary_mood']}")
        print(f"Carpet Sound: {analysis['carpet_sound']}")
        print(f"Confidence: {analysis['confidence']:.2f}")
        print(f"Trigger Words Found: {len(analysis['trigger_words'])}")
        
        if analysis['trigger_words']:
            print(f"Trigger Words:")
            for trigger in analysis['trigger_words']:
                print(f"  - '{trigger['word']}' -> {trigger['sound']} at {trigger['timing']:.1f}s")
        
        print(f"\n📝 Reasoning: {analysis['reasoning']}")
        
        # Test soundscape recommendation
        soundscape = analyzer.get_soundscape_recommendation(text)
        print(f"\n🎵 Soundscape Recommendation:")
        print(f"Carpet Tracks: {soundscape['carpet_tracks']}")
        print(f"Triggered Sounds: {len(soundscape['triggered_sounds'])}")
        print(f"Overall Mood: {soundscape['mood']}")
    
    print("\n" + "=" * 60)
    print("✅ Complete Page Analysis Test Complete!")

def test_convenience_functions():
    """Test the convenience functions"""
    
    print("\n🔧 Testing Convenience Functions")
    print("=" * 40)
    
    sample_text = """The wind howled through the mountains as the storm approached. 
    Thunder crashed overhead, and lightning illuminated the dark sky. 
    The travelers huddled together, seeking shelter from the tempest."""
    
    # Test analyze_page_complete convenience function
    print("\n📊 Using analyze_page_complete():")
    analysis = analyze_page_complete(sample_text)
    print(f"Mood: {analysis['primary_mood']}")
    print(f"Carpet Sound: {analysis['carpet_sound']}")
    print(f"Trigger Words: {len(analysis['trigger_words'])}")
    
    # Test get_soundscape_recommendation convenience function
    print("\n🎵 Using get_soundscape_recommendation():")
    soundscape = get_soundscape_recommendation(sample_text)
    print(f"Carpet Tracks: {soundscape['carpet_tracks']}")
    print(f"Triggered Sounds: {len(soundscape['triggered_sounds'])}")
    print(f"Confidence: {soundscape['confidence']:.2f}")

def test_book_analysis():
    """Test analyzing multiple pages of a book"""
    
    print("\n📚 Testing Book Analysis")
    print("=" * 30)
    
    # Simulate a book with multiple pages
    book_pages = [
        "The peaceful Shire basked in the warm sunlight. Birds sang sweetly in the trees.",
        "Dark shadows crept through the forest. Something was watching from the darkness.",
        "The epic battle raged on the bridge. Fire and thunder filled the air.",
        "Victory at last! The eagles soared overhead, carrying hope to all."
    ]
    
    analyzer = PageAnalyzer()
    analyses = analyzer.analyze_book_pages_complete(book_pages)
    
    print(f"\n📊 Book Analysis Summary:")
    print(f"Total Pages: {len(analyses)}")
    
    mood_counts = {}
    trigger_counts = []
    
    for analysis in analyses:
        mood = analysis['primary_mood']
        mood_counts[mood] = mood_counts.get(mood, 0) + 1
        trigger_counts.append(len(analysis['trigger_words']))
    
    print(f"Mood Distribution: {mood_counts}")
    print(f"Average Trigger Words per Page: {sum(trigger_counts)/len(trigger_counts):.1f}")

if __name__ == "__main__":
    test_complete_page_analysis()
    test_convenience_functions()
    test_book_analysis() 
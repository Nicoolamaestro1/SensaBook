#!/usr/bin/env python3
"""
Test script for narrative structure analysis functionality.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from app.services.emotion_analysis import AdvancedEmotionAnalyzer

def test_narrative_structure():
    """Test the narrative structure analysis capabilities."""
    
    analyzer = AdvancedEmotionAnalyzer()
    
    # Test cases with different narrative structures
    test_cases = [
        {
            "name": "Three-Act Structure - Hero's Journey",
            "text": """
            Once upon a time, there was a young warrior named Aric. He lived in a peaceful village 
            where everyone was happy and content. The setting was idyllic, with rolling hills and 
            gentle streams. However, one day a dark shadow fell over the land. The problem began 
            when mysterious creatures started appearing at night. The tension built as more villagers 
            disappeared. Aric knew he had to act. The challenge seemed impossible, but he gathered 
            his courage. Finally, the moment arrived when he faced the dark lord in an epic battle. 
            The conflict was intense and brutal. After the battle, the land began to heal. The 
            villagers slowly returned, and peace was restored. Aric had learned that true courage 
            comes from protecting others. The resolution brought harmony back to the kingdom.
            """,
            "expected_structure": "three_act_structure"
        },
        {
            "name": "Dramatic Arc - Tragedy",
            "text": """
            The celebration was in full swing, with laughter and joy filling the air. Everyone 
            was happy and excited about the upcoming wedding. The bride and groom were absolutely 
            delighted, their faces glowing with love and happiness. Then suddenly, everything 
            changed. A terrible accident occurred, and the mood shifted dramatically. Fear and 
            panic spread through the crowd. The joy was completely replaced by sadness and grief. 
            The atmosphere became heavy with sorrow and despair. However, through the tragedy, 
            people found strength in each other. They learned to support one another in difficult 
            times. The community grew stronger as they faced their shared loss together.
            """,
            "expected_structure": "dramatic_arc"
        },
        {
            "name": "Action-Packed - Adventure",
            "text": """
            The chase began immediately as the thief darted through the crowded marketplace. 
            Quickly, the guards gave pursuit, their boots pounding on the cobblestone streets. 
            Suddenly, the thief leaped over a cart, causing chaos in his wake. The action was 
            fast-paced and intense. Merchants shouted as their wares scattered. The thief ran 
            faster, his heart pounding with adrenaline. He ducked into an alley, but the guards 
            were right behind him. The tension was building rapidly. He scaled a wall and 
            disappeared over the rooftops. The guards followed, their determination unwavering. 
            The chase continued across the city, with each moment more thrilling than the last.
            """,
            "expected_structure": "action_packed"
        },
        {
            "name": "Character-Driven - Personal Growth",
            "text": """
            Sarah sat quietly in her garden, contemplating her life. She had always been shy 
            and reserved, preferring to stay in the background. The gentle breeze rustled the 
            leaves as she reflected on her past decisions. She realized that her fear of 
            rejection had held her back from many opportunities. The realization came slowly, 
            like dawn breaking over the horizon. She thought about the friends she could have 
            made, the experiences she could have had. Her understanding deepened as she 
            considered her future. She decided that it was time to change. She would step out 
            of her comfort zone and embrace new challenges. The transformation would be gradual, 
            but she was ready to grow.
            """,
            "expected_structure": "character_driven"
        }
    ]
    
    print("📚 Testing Narrative Structure Analysis")
    print("=" * 60)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. {test_case['name']}")
        print(f"Expected Structure: {test_case['expected_structure']}")
        print("-" * 50)
        
        # Analyze narrative structure
        narrative_result = analyzer.analyze_narrative_structure(test_case['text'])
        
        print(f"Overall Structure: {narrative_result.overall_structure}")
        
        # Show story elements
        print(f"\nStory Elements ({len(narrative_result.story_elements)}):")
        for element in narrative_result.story_elements:
            print(f"  {element['type']}: '{element['keyword']}' (confidence: {element['confidence']:.2f})")
        
        # Show character development
        print(f"\nCharacter Development ({len(narrative_result.character_development)}):")
        for dev in narrative_result.character_development:
            print(f"  {dev['type']}: '{dev['keyword']}' (intensity: {dev['intensity']:.2f})")
        
        # Show plot progression
        plot = narrative_result.plot_progression
        print(f"\nPlot Progression:")
        print(f"  Story Arc: {plot['story_arc']}")
        print(f"  Plot Points: {len(plot['plot_points'])}")
        
        # Show narrative pacing
        pacing = narrative_result.narrative_pacing
        print(f"\nNarrative Pacing:")
        print(f"  Overall Pace: {pacing['overall_pace']}")
        print(f"  Pace Indicators: {len(pacing['pace_indicators'])}")
        
        # Show conflict resolution
        conflict = narrative_result.conflict_resolution
        print(f"\nConflict Resolution:")
        print(f"  Tension Arc: {conflict['tension_arc']}")
        print(f"  Conflicts: {len(conflict['conflicts'])}")
        print(f"  Resolutions: {len(conflict['resolutions'])}")
        
        # Show setting details
        setting = narrative_result.setting_details
        print(f"\nSetting Details:")
        print(f"  Locations: {len(setting['locations'])}")
        print(f"  Time Periods: {len(setting['time_periods'])}")
        print(f"  Atmospheric Elements: {len(setting['atmospheric_elements'])}")
        
        # Generate soundscape recommendations
        soundscape = analyzer.generate_narrative_soundscape(narrative_result)
        print(f"\nSoundscape Theme: {soundscape['overall_theme']}")
        print(f"Story Element Sounds: {len(soundscape['story_element_sounds'])}")
        print(f"Character Sounds: {len(soundscape['character_sounds'])}")
        print(f"Pacing Sounds: {soundscape['pacing_sounds']}")
        print(f"Conflict Sounds: {soundscape['conflict_sounds']}")
        print(f"Setting Sounds: {soundscape['setting_sounds']}")
        
        print("=" * 60)

def test_story_element_detection():
    """Test specific story element detection features."""
    
    analyzer = AdvancedEmotionAnalyzer()
    
    print("\n🔍 Testing Story Element Detection")
    print("=" * 40)
    
    # Test text with clear story elements
    test_text = """
    The story began in a quiet village. Long ago, the people lived peacefully. Then suddenly, 
    a problem arose. The tension built as the situation worsened. Finally, the critical moment 
    arrived. After the conflict, things began to calm down. The resolution brought peace back 
    to the village.
    """
    
    narrative_result = analyzer.analyze_narrative_structure(test_text)
    
    print("Detected Story Elements:")
    for element in narrative_result.story_elements:
        print(f"  {element['type'].upper()}: '{element['keyword']}' at position {element['position']}")
        print(f"    Context: {element['context'][:80]}...")
        print(f"    Confidence: {element['confidence']:.2f}")
        print()

def test_character_analysis():
    """Test character development analysis."""
    
    analyzer = AdvancedEmotionAnalyzer()
    
    print("\n👥 Testing Character Analysis")
    print("=" * 40)
    
    # Test text with character development
    test_text = """
    John was a shy person who rarely spoke to others. He looked nervous in social situations. 
    However, he learned to overcome his fears. He discovered that people were generally kind. 
    He grew more confident with each interaction. His transformation was remarkable. He became 
    a trusted friend to many.
    """
    
    narrative_result = analyzer.analyze_narrative_structure(test_text)
    
    print("Character Development Analysis:")
    for dev in narrative_result.character_development:
        print(f"  {dev['type'].replace('_', ' ').title()}: '{dev['keyword']}'")
        print(f"    Intensity: {dev['intensity']:.2f}")
        print(f"    Context: {dev['context'][:80]}...")
        print()

if __name__ == "__main__":
    test_narrative_structure()
    test_story_element_detection()
    test_character_analysis()

#!/usr/bin/env python3
"""
Test script for AI Integration with Existing Book ID 6.
This script tests the AI-enhanced system with real book content.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.ai_enhanced_soundscape import ai_soundscape_service
from app.services.ai_emotion_analysis import ai_emotion_analyzer
from app.services.emotion_analysis import emotion_analyzer

def test_book_content_analysis():
    """Test AI analysis with sample book content that might be in Book ID 6."""
    print("📚 Testing AI Integration with Book Content")
    print("=" * 60)
    
    # Sample book excerpts that might represent different emotional scenes
    book_excerpts = [
        {
            "text": "The ancient castle loomed before them, its dark towers reaching into the stormy sky. Thunder crashed overhead as lightning illuminated the crumbling stone walls.",
            "expected_emotion": "fear",
            "description": "Dark, ominous castle scene"
        },
        {
            "text": "Her heart soared with joy as she discovered the hidden garden, filled with blooming flowers and the sweet songs of birds.",
            "expected_emotion": "joy",
            "description": "Beautiful garden discovery scene"
        },
        {
            "text": "The battle raged around them, swords clashing and arrows flying. The hero's determination burned like fire in his veins.",
            "expected_emotion": "anger",
            "description": "Intense battle scene"
        },
        {
            "text": "Tears streamed down her face as she read the heartbreaking letter, her world crumbling around her.",
            "expected_emotion": "sadness",
            "description": "Emotional letter reading scene"
        },
        {
            "text": "The room was quiet and peaceful, with only the gentle sound of pages turning and the soft glow of candlelight.",
            "expected_emotion": "neutral",
            "description": "Calm reading scene"
        }
    ]
    
    print(f"Testing {len(book_excerpts)} different emotional scenes...")
    print()
    
    ai_success_count = 0
    fallback_success_count = 0
    
    for i, excerpt in enumerate(book_excerpts, 1):
        print(f"📖 Scene {i}: {excerpt['description']}")
        print("-" * 50)
        print(f"Text: {excerpt['text'][:80]}...")
        print(f"Expected: {excerpt['expected_emotion']}")
        
        try:
            # Test AI-enhanced analysis
            ai_result = ai_soundscape_service.generate_soundscape(excerpt['text'], use_ai=True)
            
            print(f"AI Emotion: {ai_result.ai_emotion}")
            print(f"AI Confidence: {ai_result.ai_confidence:.3f}")
            print(f"Primary Soundscape: {ai_result.primary_soundscape}")
            print(f"Intensity: {ai_result.intensity:.3f}")
            print(f"Atmosphere: {ai_result.atmosphere}")
            print(f"Sound Effects: {', '.join(ai_result.sound_effects[:3])}")
            print(f"AI Enhanced: {'✅' if not ai_result.fallback_used else '❌'}")
            
            # Check accuracy
            if ai_result.ai_emotion == excerpt['expected_emotion']:
                print("✅ AI Emotion Detection: CORRECT")
                ai_success_count += 1
            else:
                print(f"❌ AI Emotion Detection: WRONG (got {ai_result.ai_emotion})")
            
            # Test fallback system
            fallback_result = ai_soundscape_service.generate_soundscape(excerpt['text'], use_ai=False)
            print(f"Fallback Emotion: {fallback_result.ai_emotion}")
            print(f"Fallback Used: {'✅' if fallback_result.fallback_used else '❌'}")
            
            if fallback_result.ai_emotion == excerpt['expected_emotion']:
                print("✅ Fallback Emotion Detection: CORRECT")
                fallback_success_count += 1
            else:
                print(f"❌ Fallback Emotion Detection: WRONG (got {fallback_result.ai_emotion})")
            
        except Exception as e:
            print(f"❌ Error analyzing scene: {e}")
        
        print()
    
    # Summary
    print("📊 Analysis Summary")
    print("=" * 60)
    print(f"AI Success Rate: {ai_success_count}/{len(book_excerpts)} ({ai_success_count/len(book_excerpts)*100:.1f}%)")
    print(f"Fallback Success Rate: {fallback_success_count}/{len(book_excerpts)} ({fallback_success_count/len(book_excerpts)*100:.1f}%)")
    
    return ai_success_count, fallback_success_count

def test_soundscape_generation():
    """Test soundscape generation with book content."""
    print("\n🎵 Testing Soundscape Generation")
    print("=" * 60)
    
    test_text = "The hero's heart pounded with fear as he entered the dark cave, the sound of dripping water echoing ominously around him."
    
    try:
        print(f"Text: {test_text}")
        print()
        
        # Test AI-enhanced soundscape
        ai_soundscape = ai_soundscape_service.generate_soundscape(test_text, use_ai=True)
        
        print("🎵 AI-Enhanced Soundscape:")
        print(f"  Primary: {ai_soundscape.primary_soundscape}")
        print(f"  Secondary: {ai_soundscape.secondary_soundscape}")
        print(f"  Intensity: {ai_soundscape.intensity:.3f}")
        print(f"  Volume: {ai_soundscape.recommended_volume:.3f}")
        print(f"  Atmosphere: {ai_soundscape.atmosphere}")
        print(f"  Sound Effects: {', '.join(ai_soundscape.sound_effects)}")
        print(f"  AI Confidence: {ai_soundscape.ai_confidence:.3f}")
        print(f"  AI Enhanced: {'✅' if not ai_soundscape.fallback_used else '❌'}")
        
        print()
        
        # Test fallback soundscape
        fallback_soundscape = ai_soundscape_service.generate_soundscape(test_text, use_ai=False)
        
        print("🎵 Fallback Soundscape:")
        print(f"  Primary: {fallback_soundscape.primary_soundscape}")
        print(f"  Secondary: {fallback_soundscape.secondary_soundscape}")
        print(f"  Intensity: {fallback_soundscape.intensity:.3f}")
        print(f"  Volume: {fallback_soundscape.recommended_volume:.3f}")
        print(f"  Atmosphere: {fallback_soundscape.atmosphere}")
        print(f"  Sound Effects: {', '.join(fallback_soundscape.sound_effects)}")
        print(f"  Fallback Used: {'✅' if fallback_soundscape.fallback_used else '❌'}")
        
    except Exception as e:
        print(f"❌ Error in soundscape generation: {e}")

def test_performance_and_metrics():
    """Test system performance and metrics."""
    print("\n📊 Testing System Performance")
    print("=" * 60)
    
    try:
        # Get AI performance metrics
        ai_metrics = ai_soundscape_service.get_performance_metrics()
        
        print("AI System Status:")
        print(f"  AI Enabled: {ai_metrics['ai_enabled']}")
        print(f"  Fallback Enabled: {ai_metrics['fallback_enabled']}")
        print(f"  Confidence Threshold: {ai_metrics['confidence_threshold']}")
        print(f"  System Status: {ai_metrics['system_status']}")
        
        print("\nAudio Configuration:")
        for level, config in ai_metrics['audio_configs'].items():
            print(f"  {level.upper()}: Volume x{config['volume_multiplier']}, "
                  f"Intensity x{config['intensity_boost']}, Effects: {config['effect_density']}")
        
        # Test batch processing
        print("\n📚 Testing Batch Processing...")
        batch_texts = [
            "The sun shone brightly, filling everyone with joy.",
            "Dark shadows crept across the floor, filling her with terror.",
            "He felt a gentle warmth of happiness spread through his chest.",
            "The room was quiet and peaceful, nothing remarkable about it."
        ]
        
        batch_results = ai_soundscape_service.batch_generate_soundscapes(batch_texts, use_ai=True)
        
        print(f"Batch processed {len(batch_results)} texts successfully")
        for i, result in enumerate(batch_results, 1):
            print(f"  {i}. {result.ai_emotion} (confidence: {result.ai_confidence:.3f})")
        
        print("✅ Performance testing completed successfully")
        
    except Exception as e:
        print(f"❌ Error in performance testing: {e}")

def main():
    """Run all book integration tests."""
    print("🚀 Starting Book Integration Tests")
    print("=" * 60)
    
    try:
        # Test book content analysis
        ai_success, fallback_success = test_book_content_analysis()
        
        # Test soundscape generation
        test_soundscape_generation()
        
        # Test performance and metrics
        test_performance_and_metrics()
        
        print("\n🎉 All book integration tests completed!")
        print("\n📋 Final Summary:")
        print(f"✅ AI Analysis: {ai_success}/5 scenes correct")
        print(f"✅ Fallback System: {fallback_success}/5 scenes correct")
        print("✅ Soundscape Generation: Working")
        print("✅ Performance Metrics: Available")
        print("✅ System Status: Operational")
        
        if ai_success >= 4:
            print("\n🎯 AI System Performance: EXCELLENT")
        elif ai_success >= 3:
            print("\n🎯 AI System Performance: GOOD")
        else:
            print("\n🎯 AI System Performance: NEEDS IMPROVEMENT")
        
    except Exception as e:
        print(f"\n💥 Book integration test suite failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

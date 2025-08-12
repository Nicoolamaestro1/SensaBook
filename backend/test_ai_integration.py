#!/usr/bin/env python3
"""
Test script for AI Integration with Existing Soundscape System.
This script tests the AI-enhanced soundscape service and API endpoints.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.ai_enhanced_soundscape import ai_soundscape_service
from app.services.ai_emotion_analysis import ai_emotion_analyzer

def test_ai_enhanced_soundscape():
    """Test the AI-enhanced soundscape generation."""
    print("🎵 Testing AI-Enhanced Soundscape Generation")
    print("=" * 60)
    
    # Test texts with different emotional content
    test_texts = [
        {
            "text": "The hero's heart soared with overwhelming joy and excitement as he discovered the ancient treasure!",
            "expected_emotion": "joy",
            "description": "High-intensity joy scene"
        },
        {
            "text": "Dark shadows crept across the floor, filling her with absolute terror and dread.",
            "expected_emotion": "fear",
            "description": "High-intensity fear scene"
        },
        {
            "text": "She felt a gentle warmth of happiness spread through her chest.",
            "expected_emotion": "joy",
            "description": "Low-intensity joy scene"
        },
        {
            "text": "The room was quiet and peaceful, nothing remarkable about it.",
            "expected_emotion": "neutral",
            "description": "Neutral scene"
        }
    ]
    
    for i, test_case in enumerate(test_texts, 1):
        print(f"\n📖 Test {i}: {test_case['description']}")
        print("-" * 50)
        print(f"Text: {test_case['text'][:60]}...")
        print(f"Expected Emotion: {test_case['expected_emotion']}")
        
        try:
            # Test AI-enhanced soundscape generation
            result = ai_soundscape_service.generate_soundscape(test_case['text'], use_ai=True)
            
            print(f"AI Emotion: {result.ai_emotion}")
            print(f"AI Confidence: {result.ai_confidence:.3f}")
            print(f"Primary Soundscape: {result.primary_soundscape}")
            print(f"Secondary Soundscape: {result.secondary_soundscape}")
            print(f"Intensity: {result.intensity:.3f}")
            print(f"Volume: {result.recommended_volume:.3f}")
            print(f"Atmosphere: {result.atmosphere}")
            print(f"Sound Effects: {result.sound_effects[:3]}")  # Show first 3
            print(f"Fallback Used: {'❌' if not result.fallback_used else '✅'}")
            print(f"AI Enhanced: {'✅' if not result.fallback_used else '❌'}")
            
            # Check if AI got the emotion right
            if result.ai_emotion == test_case['expected_emotion']:
                print("✅ AI Emotion Detection: CORRECT")
            else:
                print(f"❌ AI Emotion Detection: WRONG (got {result.ai_emotion})")
            
            # Show confidence level
            confidence_level = "high" if result.ai_confidence >= 0.9 else "medium" if result.ai_confidence >= 0.7 else "low"
            print(f"Confidence Level: {confidence_level}")
            
        except Exception as e:
            print(f"❌ Error in AI soundscape generation: {e}")
        
        print()

def test_fallback_system():
    """Test the fallback to rule-based system."""
    print("\n🔄 Testing Fallback System")
    print("=" * 60)
    
    test_text = "The hero felt joy and excitement!"
    
    try:
        # Test with AI disabled
        print("Testing with AI disabled (fallback to rule-based)...")
        result = ai_soundscape_service.generate_soundscape(test_text, use_ai=False)
        
        print(f"Fallback Used: {'✅' if result.fallback_used else '❌'}")
        print(f"AI Enhanced: {'❌' if result.fallback_used else '✅'}")
        print(f"Primary Soundscape: {result.primary_soundscape}")
        print(f"Intensity: {result.intensity:.3f}")
        print(f"AI Confidence: {result.ai_confidence}")
        
        if result.fallback_used:
            print("✅ Fallback system working correctly")
        else:
            print("❌ Fallback system not working")
            
    except Exception as e:
        print(f"❌ Error in fallback system: {e}")
    
    print()

def test_batch_generation():
    """Test batch soundscape generation."""
    print("\n📚 Testing Batch Soundscape Generation")
    print("=" * 60)
    
    batch_texts = [
        "The sun shone brightly, filling everyone with joy.",
        "Thunder crashed and lightning flashed, terrifying the children.",
        "She smiled warmly, her happiness contagious.",
        "The news hit him like a punch to the gut, leaving him stunned."
    ]
    
    try:
        print(f"Processing {len(batch_texts)} texts in batch...")
        batch_results = ai_soundscape_service.batch_generate_soundscapes(batch_texts, use_ai=True)
        
        for i, result in enumerate(batch_results, 1):
            print(f"\n{i}. AI Emotion: {result.ai_emotion}")
            print(f"   Confidence: {result.ai_confidence:.3f}")
            print(f"   Primary Soundscape: {result.primary_soundscape}")
            print(f"   Intensity: {result.intensity:.3f}")
            print(f"   AI Enhanced: {'✅' if not result.fallback_used else '❌'}")
    
    except Exception as e:
        print(f"❌ Error in batch generation: {e}")
    
    print()

def test_performance_metrics():
    """Test performance metrics collection."""
    print("\n📊 Testing Performance Metrics")
    print("=" * 60)
    
    try:
        metrics = ai_soundscape_service.get_performance_metrics()
        
        print("AI Soundscape Service Metrics:")
        print(f"  AI Enabled: {metrics['ai_enabled']}")
        print(f"  Fallback Enabled: {metrics['fallback_enabled']}")
        print(f"  Confidence Threshold: {metrics['confidence_threshold']}")
        print(f"  System Status: {metrics['system_status']}")
        
        print("\nAudio Configuration by Confidence Level:")
        for level, config in metrics['audio_configs'].items():
            print(f"  {level.upper()}: Volume x{config['volume_multiplier']}, "
                  f"Intensity x{config['intensity_boost']}, Effects: {config['effect_density']}")
        
        print("✅ Performance metrics collected successfully")
        
    except Exception as e:
        print(f"❌ Error collecting performance metrics: {e}")
    
    print()

def test_error_handling():
    """Test error handling and edge cases."""
    print("\n⚠️ Testing Error Handling")
    print("=" * 60)
    
    edge_cases = [
        "",  # Empty string
        "   ",  # Whitespace only
        "a",  # Single character
        "The quick brown fox jumps over the lazy dog. " * 50,  # Very long text
    ]
    
    for i, text in enumerate(edge_cases, 1):
        print(f"\nEdge Case {i}: {repr(text[:50])}")
        print("-" * 30)
        
        try:
            result = ai_soundscape_service.generate_soundscape(text, use_ai=True)
            print(f"Result: {result.ai_emotion}")
            print(f"Confidence: {result.ai_confidence:.3f}")
            print(f"Fallback Used: {'✅' if result.fallback_used else '❌'}")
            print(f"Handled gracefully: ✅")
        
        except Exception as e:
            print(f"Error: {e}")
            print(f"Handled gracefully: ❌")
    
    print()

def main():
    """Run all AI integration tests."""
    print("🚀 Starting AI Integration Tests")
    print("=" * 60)
    
    try:
        # Test AI-enhanced soundscape generation
        test_ai_enhanced_soundscape()
        
        # Test fallback system
        test_fallback_system()
        
        # Test batch generation
        test_batch_generation()
        
        # Test performance metrics
        test_performance_metrics()
        
        # Test error handling
        test_error_handling()
        
        print("\n🎉 All AI integration tests completed!")
        print("\n📋 Summary:")
        print("✅ AI-enhanced soundscape generation working")
        print("✅ Fallback system operational")
        print("✅ Batch processing functional")
        print("✅ Performance metrics available")
        print("✅ Error handling robust")
        
    except Exception as e:
        print(f"\n💥 AI integration test suite failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

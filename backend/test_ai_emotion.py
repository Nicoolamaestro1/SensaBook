#!/usr/bin/env python3
"""
Test script for the AI Emotion Analyzer.
This script tests the AI-powered emotion analysis with various book excerpts.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.ai_emotion_analysis import AIEmotionAnalyzer, ai_emotion_analyzer
from app.services.emotion_analysis import emotion_analyzer

def test_ai_emotion_analyzer():
    """Test the AI emotion analyzer with sample texts."""
    print("🧠 Testing AI Emotion Analyzer")
    print("=" * 60)
    
    # Sample book excerpts for testing
    test_texts = [
        {
            "text": "The hero's heart soared as he beheld the ancient treasure, his eyes wide with wonder and excitement. The golden light reflected in his gaze, filling him with an overwhelming sense of joy.",
            "expected_emotion": "joy",
            "description": "Adventure scene with discovery and excitement"
        },
        {
            "text": "Dark shadows crept across the floor, and a cold dread settled in her stomach as footsteps echoed in the distance. Her heart pounded like a drum, each beat louder than the last.",
            "expected_emotion": "fear",
            "description": "Horror scene with building suspense"
        },
        {
            "text": "She felt a warm glow of happiness spread through her chest, like sunlight breaking through clouds after a long storm. Her smile was genuine and pure.",
            "expected_emotion": "joy",
            "description": "Peaceful, happy moment"
        },
        {
            "text": "Rage burned within him like a wildfire, consuming all reason and logic. His fists clenched so tightly that his nails dug into his palms, drawing blood.",
            "expected_emotion": "anger",
            "description": "Intense anger and rage"
        },
        {
            "text": "Tears streamed down her face as she clutched the letter, her world shattering into a million pieces. The pain was so deep it felt like her heart was being torn apart.",
            "expected_emotion": "sadness",
            "description": "Deep sadness and grief"
        },
        {
            "text": "Suddenly, without warning, the door burst open and a figure appeared in the doorway. She jumped back in shock, her eyes wide with surprise.",
            "expected_emotion": "surprise",
            "description": "Sudden surprise and shock"
        },
        {
            "text": "The smell was absolutely revolting, making her stomach churn. She covered her nose and mouth, trying not to gag at the putrid stench.",
            "expected_emotion": "disgust",
            "description": "Physical disgust and revulsion"
        },
        {
            "text": "The room was quiet and peaceful, with nothing particularly remarkable about it. It was just an ordinary day with ordinary thoughts.",
            "expected_emotion": "neutral",
            "description": "Neutral, calm description"
        }
    ]
    
    # Test each text
    for i, test_case in enumerate(test_texts, 1):
        print(f"\n📖 Test {i}: {test_case['description']}")
        print("-" * 50)
        print(f"Text: {test_case['text'][:80]}...")
        print(f"Expected: {test_case['expected_emotion']}")
        
        try:
            # Test AI analysis
            ai_result = ai_emotion_analyzer.analyze_emotion(test_case['text'])
            
            print(f"AI Result: {ai_result.primary_emotion.value}")
            print(f"AI Confidence: {ai_result.confidence:.3f}")
            print(f"AI Scores: {dict(list(ai_result.emotion_scores.items())[:3])}")  # Show top 3
            
            # Check if AI got it right
            if ai_result.primary_emotion.value == test_case['expected_emotion']:
                print("✅ AI Analysis: CORRECT")
            else:
                print(f"❌ AI Analysis: WRONG (got {ai_result.primary_emotion.value})")
            
            # Show raw predictions
            print(f"Raw Predictions: {dict(list(ai_result.raw_predictions.items())[:3])}")
            
        except Exception as e:
            print(f"❌ Error in AI analysis: {e}")
        
        print()

def compare_ai_vs_rule_based():
    """Compare AI results with the old rule-based system."""
    print("\n🔄 Comparing AI vs Rule-Based Analysis")
    print("=" * 60)
    
    # Sample texts for comparison
    comparison_texts = [
        "The hero's heart soared with joy and excitement!",
        "Dark shadows filled her with terror and fear.",
        "She felt overwhelming sadness and despair.",
        "His anger burned like fire, consuming everything."
    ]
    
    for i, text in enumerate(comparison_texts, 1):
        print(f"\n📝 Comparison {i}: {text}")
        print("-" * 40)
        
        try:
            # Get AI result
            ai_result = ai_emotion_analyzer.analyze_emotion(text)
            
            # Get rule-based result (using your existing system)
            rule_result = emotion_analyzer.analyze_emotion(text)
            
            # Compare results
            comparison = ai_emotion_analyzer.compare_with_rule_based(text, rule_result)
            
            print(f"AI Emotion: {comparison['ai_emotion']} (confidence: {comparison['ai_confidence']:.3f})")
            print(f"Rule-Based: {comparison['rule_based_emotion']}")
            print(f"Agreement: {'✅ YES' if comparison['agreement'] else '❌ NO'}")
            
            if not comparison['agreement']:
                print(f"AI Scores: {comparison['ai_scores']}")
                print(f"Raw AI Predictions: {comparison['raw_predictions']}")
        
        except Exception as e:
            print(f"❌ Error in comparison: {e}")
        
        print()

def test_batch_analysis():
    """Test batch processing of multiple texts."""
    print("\n📚 Testing Batch Analysis")
    print("=" * 60)
    
    batch_texts = [
        "The sun shone brightly, filling everyone with joy.",
        "Thunder crashed and lightning flashed, terrifying the children.",
        "She smiled warmly, her happiness contagious.",
        "The news hit him like a punch to the gut, leaving him stunned."
    ]
    
    try:
        print(f"Processing {len(batch_texts)} texts in batch...")
        batch_results = ai_emotion_analyzer.batch_analyze(batch_texts)
        
        for i, (text, result) in enumerate(zip(batch_texts, batch_results)):
            print(f"\n{i+1}. {text[:50]}...")
            print(f"   Emotion: {result.primary_emotion.value}")
            print(f"   Confidence: {result.confidence:.3f}")
    
    except Exception as e:
        print(f"❌ Error in batch analysis: {e}")

def test_error_handling():
    """Test how the system handles edge cases and errors."""
    print("\n⚠️ Testing Error Handling")
    print("=" * 60)
    
    edge_cases = [
        "",  # Empty string
        "   ",  # Whitespace only
        "a",  # Single character
        "The quick brown fox jumps over the lazy dog. " * 100,  # Very long text
    ]
    
    for i, text in enumerate(edge_cases, 1):
        print(f"\nEdge Case {i}: {repr(text[:50])}")
        print("-" * 30)
        
        try:
            result = ai_emotion_analyzer.analyze_emotion(text)
            print(f"Result: {result.primary_emotion.value}")
            print(f"Confidence: {result.confidence:.3f}")
            print(f"Handled gracefully: ✅")
        
        except Exception as e:
            print(f"Error: {e}")
            print(f"Handled gracefully: ❌")

def main():
    """Run all tests."""
    print("🚀 Starting AI Emotion Analyzer Tests")
    print("=" * 60)
    
    try:
        # Test basic functionality
        test_ai_emotion_analyzer()
        
        # Test comparison with rule-based system
        compare_ai_vs_rule_based()
        
        # Test batch processing
        test_batch_analysis()
        
        # Test error handling
        test_error_handling()
        
        print("\n🎉 All tests completed!")
        
    except Exception as e:
        print(f"\n💥 Test suite failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Test script to verify carpet sounds are working with restored SCENE_SOUND_MAPPINGS
"""

import requests
import json

def test_carpet_sounds():
    """Test carpet sound detection for different pages"""
    
    print("🧪 Testing Carpet Sound Restoration")
    print("=" * 50)
    
    # Test different pages
    test_pages = [
        (4, 1, 1, "First page"),
        (4, 1, 2, "Second page"), 
        (4, 1, 3, "Third page"),
    ]
    
    for book_id, chapter, page, description in test_pages:
        try:
            response = requests.get(f'http://localhost:8000/soundscape/book/{book_id}/chapter{chapter}/page/{page}')
            
            if response.status_code == 200:
                data = response.json()
                carpet_tracks = data.get('carpet_tracks', [])
                detected_scenes = data.get('detected_scenes', [])
                summary = data.get('summary', 'No summary')
                
                print(f"\n📖 {description} (Book {book_id}, Chapter {chapter}, Page {page}):")
                print(f"   Carpet Tracks: {carpet_tracks}")
                print(f"   Detected Scenes: {detected_scenes}")
                print(f"   Summary: {summary}")
                
                if carpet_tracks:
                    print(f"   ✅ CARPET SOUND WORKING: {carpet_tracks[0]}")
                else:
                    print(f"   ❌ NO CARPET SOUND DETECTED")
                    
            else:
                print(f"\n❌ Error for {description}: Status {response.status_code}")
                
        except Exception as e:
            print(f"\n❌ Exception for {description}: {e}")
    
    print("\n" + "=" * 50)
    print("✅ Carpet Sound Test Complete!")

if __name__ == "__main__":
    test_carpet_sounds() 
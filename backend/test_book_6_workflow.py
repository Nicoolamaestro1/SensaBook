#!/usr/bin/env python3
"""
Test Book ID 6 Full Workflow
Tests all pages with the new smart soundscape system
"""

import requests
import json
import time
from typing import Dict, List

def test_book_6_workflow():
    """Test the complete workflow for book ID 6."""
    base_url = "http://localhost:8000"
    
    print("🚀 Testing Book ID 6 Full Workflow")
    print("=" * 60)
    
    # Test different page combinations for book 6
    test_cases = [
        {"book_id": 6, "chapter": 1, "page": 1},
        {"book_id": 6, "chapter": 1, "page": 2},
        {"book_id": 6, "chapter": 1, "page": 3},
        {"book_id": 6, "chapter": 2, "page": 1},
        {"book_id": 6, "chapter": 2, "page": 2},
        {"book_id": 6, "chapter": 3, "page": 1},
    ]
    
    results = []
    
    for test_case in test_cases:
        print(f"\n📖 Testing Book {test_case['book_id']}, Chapter {test_case['chapter']}, Page {test_case['page']}")
        print("-" * 50)
        
        try:
            # Test the soundscape endpoint
            url = f"{base_url}/soundscape/book/{test_case['book_id']}/chapter/{test_case['chapter']}/page/{test_case['page']}"
            
            print(f"URL: {url}")
            
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                print("✅ Success!")
                
                # Extract key information
                soundscape = data.get("soundscape", {})
                
                print(f"Scene Type: {soundscape.get('scene_type', 'N/A')}")
                print(f"Primary Audio: {soundscape.get('primary_audio', 'N/A')}")
                print(f"Secondary Audio: {soundscape.get('secondary_audio', 'N/A')}")
                print(f"Mood: {soundscape.get('mood', 'N/A')}")
                print(f"Intensity: {soundscape.get('intensity', 'N/A')}")
                print(f"Confidence: {soundscape.get('confidence', 'N/A')}")
                print(f"Reasoning: {soundscape.get('reasoning', 'N/A')[:100]}...")
                
                # Check if it's working correctly
                if soundscape.get('primary_audio') and soundscape.get('scene_type'):
                    print("✅ Smart soundscape working correctly")
                else:
                    print("❌ Missing key soundscape data")
                
                results.append({
                    "test_case": test_case,
                    "status": "success",
                    "data": soundscape
                })
                
            else:
                print(f"❌ HTTP Error: {response.status_code}")
                print(f"Response: {response.text}")
                
                results.append({
                    "test_case": test_case,
                    "status": "error",
                    "error": f"HTTP {response.status_code}: {response.text}"
                })
                
        except requests.exceptions.ConnectionError:
            print("❌ Connection Error - Server might not be running")
            print("Make sure to start the server with: python -m uvicorn app.main:app --reload")
            break
            
        except requests.exceptions.Timeout:
            print("❌ Timeout Error - Request took too long")
            
        except Exception as e:
            print(f"❌ Unexpected Error: {e}")
            
        # Small delay between requests
        time.sleep(1)
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 WORKFLOW TEST SUMMARY")
    print("=" * 60)
    
    successful_tests = [r for r in results if r["status"] == "success"]
    failed_tests = [r for r in results if r["status"] == "error"]
    
    print(f"Total Tests: {len(results)}")
    print(f"Successful: {len(successful_tests)}")
    print(f"Failed: {len(failed_tests)}")
    
    if successful_tests:
        print("\n✅ SUCCESSFUL TESTS:")
        for result in successful_tests:
            test_case = result["test_case"]
            data = result["data"]
            print(f"  Book {test_case['book_id']}, Ch {test_case['chapter']}, Pg {test_case['page']}: {data.get('scene_type', 'N/A')} -> {data.get('primary_audio', 'N/A')}")
    
    if failed_tests:
        print("\n❌ FAILED TESTS:")
        for result in failed_tests:
            test_case = result["test_case"]
            error = result["error"]
            print(f"  Book {test_case['book_id']}, Ch {test_case['chapter']}, Pg {test_case['page']}: {error}")
    
    # Check for Dracula problem solution
    print("\n🔍 DRACULA PROBLEM CHECK:")
    dracula_solved = True
    
    for result in successful_tests:
        data = result["data"]
        scene_type = data.get('scene_type', '')
        primary_audio = data.get('primary_audio', '')
        
        # Check if dialogue scenes get conversation audio
        if scene_type == 'dialogue' and 'conversation' not in primary_audio:
            print(f"  ❌ Dialogue scene got wrong audio: {primary_audio}")
            dracula_solved = False
        
        # Check if descriptive scenes get appropriate audio
        if scene_type == 'descriptive':
            if 'hotel' in str(data.get('reasoning', '')).lower() and 'hotel_dining' not in primary_audio:
                print(f"  ❌ Hotel scene got wrong audio: {primary_audio}")
                dracula_solved = False
    
    if dracula_solved:
        print("  ✅ Dracula problem appears to be solved!")
    else:
        print("  ❌ Dracula problem still exists")
    
    print("\n🏁 Workflow test completed!")

if __name__ == "__main__":
    print("Starting Book ID 6 Workflow Test...")
    print("Make sure the server is running on http://localhost:8000")
    print("=" * 60)
    
    # Wait a moment for server to start
    time.sleep(2)
    
    test_book_6_workflow()

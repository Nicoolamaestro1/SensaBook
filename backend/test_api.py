#!/usr/bin/env python3

import requests
import json
import time
from typing import Dict, Any

BASE_URL = "http://localhost:8000"

def test_authentication():
    """Test user registration and login"""
    print("🔐 Testing Authentication...")
    
    # Use timestamp to make email unique
    timestamp = int(time.time())
    email = f"test{timestamp}@example.com"
    
    # Register a new user
    register_data = {
        "email": email,
        "name": "Test User",
        "password": "testpassword123"
    }
    
    response = requests.post(f"{BASE_URL}/auth/register", json=register_data)
    print(f"Register Response: {response.status_code}")
    if response.status_code == 200:
        print("✅ User registered successfully!")
        user_data = response.json()
        print(f"User ID: {user_data.get('id')}")
    else:
        print(f"❌ Registration failed: {response.text}")
        return None
    
    # Login to get access token
    login_data = {
        "email": email,
        "password": "testpassword123"
    }
    
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    print(f"Login Response: {response.status_code}")
    if response.status_code == 200:
        print("✅ Login successful!")
        token_data = response.json()
        access_token = token_data.get("access_token")
        print(f"Access Token: {access_token[:20]}...")
        return access_token
    else:
        print(f"❌ Login failed: {response.text}")
        return None

def test_emotion_analysis(token: str):
    print("\n🧠 Testing Revolutionary Emotion Analysis...")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test different types of text
    test_texts = [
        "I was so happy and excited to see my friends! We laughed and celebrated together.",
        "The dark forest was terrifying. I felt afraid and scared as the shadows moved.",
        "I was furious and angry when I discovered the betrayal. My rage knew no bounds.",
        "The magical castle stood majestically on the mountain peak, surrounded by enchanted forests."
    ]
    
    for i, text in enumerate(test_texts, 1):
        print(f"\n📝 Test Text {i}: {text[:50]}...")
        
        response = requests.post(
            f"{BASE_URL}/api/analytics/analyze-emotion",
            headers=headers,
            params={"text": text}
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Primary Emotion: {result['primary_emotion']}")
            print(f"   Intensity: {result['intensity']:.2f}")
            print(f"   Keywords: {result['keywords']}")
        else:
            print(f"❌ Emotion analysis failed: {response.text}")

def test_theme_analysis(token: str):
    print("\n🎭 Testing Revolutionary Theme Analysis...")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    test_text = "The brave knight embarked on a dangerous quest through the enchanted forest, seeking the magical treasure hidden in the ancient castle."
    
    response = requests.post(
        f"{BASE_URL}/api/analytics/analyze-theme",
        headers=headers,
        params={"text": test_text}
    )
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Primary Theme: {result['primary_theme']}")
        print(f"   Atmosphere: {result['atmosphere']}")
        print(f"   Setting Elements: {result['setting_elements']}")
    else:
        print(f"❌ Theme analysis failed: {response.text}")

def test_soundscape_generation(token: str):
    print("\n🎵 Testing Revolutionary Soundscape Generation...")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    test_text = "The thunder crashed and lightning flashed as the storm raged through the dark night. The old castle creaked ominously."
    
    response = requests.post(
        f"{BASE_URL}/api/analytics/generate-soundscape",
        headers=headers,
        params={"text": test_text}
    )
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Primary Soundscape: {result['primary_soundscape']}")
        print(f"   Secondary Soundscape: {result['secondary_soundscape']}")
        print(f"   Intensity: {result['intensity']:.2f}")
        print(f"   Recommended Volume: {result['recommended_volume']:.2f}")
        print(f"   Sound Effects: {result['sound_effects']}")
    else:
        print(f"❌ Soundscape generation failed: {response.text}")

def test_reading_analytics(token: str):
    print("\n📊 Testing Revolutionary Reading Analytics...")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Get user reading stats
    response = requests.get(
        f"{BASE_URL}/api/analytics/me/stats",
        headers=headers
    )
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Total Books Read: {result['total_books_read']}")
        print(f"   Total Pages Read: {result['total_pages_read']}")
        print(f"   Average Reading Speed: {result['average_reading_speed_wpm']} WPM")
        print(f"   Current Streak: {result['current_streak_days']} days")
        print(f"   Favorite Genres: {result['favorite_genres']}")
    else:
        print(f"❌ Reading stats failed: {response.text}")
    
    # Get book recommendations
    response = requests.get(
        f"{BASE_URL}/api/analytics/me/recommendations",
        headers=headers
    )
    
    if response.status_code == 200:
        recommendations = response.json()
        print(f"✅ Book Recommendations: {len(recommendations)} books")
        for rec in recommendations[:3]:  # Show first 3
            print(f"   - {rec['title']} by {rec['author']} ({rec['genre']})")
    else:
        print(f"❌ Recommendations failed: {response.text}")

def test_reading_patterns(token: str):
    print("\n📈 Testing Revolutionary Reading Pattern Analysis...")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.get(
        f"{BASE_URL}/api/analytics/me/patterns",
        headers=headers
    )
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Peak Reading Times: {result['peak_reading_times']}")
        print(f"   Preferred Session Length: {result['preferred_session_length']}")
        print(f"   Reading Speed Trends: {result['reading_speed_trends']}")
        print(f"   Consistency Score: {result['consistency_score']:.2f}")
    else:
        print(f"❌ Pattern analysis failed: {response.text}")

def test_create_sample_book():
    """Create a sample book with trigger words for testing position-based sounds"""
    print("📚 Creating sample book with trigger words...")
    
    # Create book
    book_data = {
        "title": "The Mysterious Mountain",
        "author": "Test Author",
        "summary": "A thrilling adventure with atmospheric sounds",
        "chapters": [
            {
                "chapter_number": 1,
                "title": "The Storm Approaches",
                "pages": [
                    {
                        "page_number": 1,
                        "content": "The wind howled through the ancient trees as dark clouds gathered overhead. Sarah could hear the distant rumble of thunder echoing across the valley. She quickened her pace, her footsteps crunching on the gravel path. The storm was approaching fast, and she needed to reach the old cabin before the rain began to fall."
                    },
                    {
                        "page_number": 2,
                        "content": "As she climbed higher into the mountains, the wind grew stronger, whipping through her hair and making the trees sway violently. Another crack of thunder split the sky, followed by the sound of footsteps approaching from behind. Sarah's heart raced as she turned to see who was following her through the storm."
                    },
                    {
                        "page_number": 3,
                        "content": "The rain finally began to fall, heavy drops pounding against the rocky terrain. The wind carried the sound of distant thunder, creating an eerie atmosphere. Sarah could hear more footsteps now, but they seemed to be coming from multiple directions. The storm had transformed the peaceful mountain into a place of mystery and danger."
                    }
                ]
            },
            {
                "chapter_number": 2,
                "title": "The Cabin",
                "pages": [
                    {
                        "page_number": 1,
                        "content": "The old cabin stood silent against the raging storm. Wind battered its weathered walls, and rain poured from the roof in steady streams. Sarah could hear the thunder growing louder as she approached the door. Inside, she hoped to find shelter from the storm and answers to the mysterious footsteps."
                    },
                    {
                        "page_number": 2,
                        "content": "As she stepped inside, the wind howled through the broken windows, carrying with it the sound of rain and distant thunder. Her footsteps echoed on the wooden floor, mixing with the storm's symphony. The cabin seemed to breathe with the rhythm of the wind, creating an atmosphere of both comfort and unease."
                    },
                    {
                        "page_number": 3,
                        "content": "The storm outside reached its peak, with thunder shaking the very foundations of the cabin. Rain pounded against the roof like a thousand tiny footsteps, while the wind continued its relentless assault. Sarah sat by the fire, listening to the storm's powerful display of nature's fury."
                    }
                ]
            },
            {
                "chapter_number": 3,
                "title": "The Revelation",
                "pages": [
                    {
                        "page_number": 1,
                        "content": "As the storm began to subside, Sarah heard footsteps approaching the cabin door. The wind had died down, but the rain still fell gently. Thunder rumbled in the distance, a reminder of the storm's power. She held her breath, waiting to see who would emerge from the storm."
                    },
                    {
                        "page_number": 2,
                        "content": "The door creaked open, and the wind rushed in one final time. Footsteps echoed through the cabin as a figure emerged from the storm. The rain had soaked their clothes, and the wind had tousled their hair. Sarah recognized the face immediately - it was her long-lost brother, returning from his mountain expedition."
                    },
                    {
                        "page_number": 3,
                        "content": "The storm had brought them together again, its wind and rain and thunder serving as the backdrop to their reunion. The footsteps that had seemed so mysterious were now familiar and welcome. The mountain had revealed its secrets through the power of the storm, and Sarah knew she would never forget this night."
                    }
                ]
            }
        ]
    }
    
    response = requests.post("http://localhost:8000/api/book", json=book_data)
    if response.status_code == 200:
        book_id = response.json()["book_id"]
        print(f"✅ Sample book created with ID: {book_id}")
        print(f"🌐 Test the position-based sounds at: http://localhost:8081/book/{book_id}")
        print("🎯 Trigger words in the book: thunder, rain, wind, footsteps, storm")
        return book_id
    else:
        print(f"❌ Failed to create sample book: {response.status_code}")
        return None

def main():
    print("🚀 SensaBook Revolutionary API Test Suite")
    print("=" * 50)
    
    # Test authentication
    token = test_authentication()
    if not token:
        print("❌ Authentication failed. Cannot proceed with tests.")
        return
    
    # Test all revolutionary features
    test_emotion_analysis(token)
    test_theme_analysis(token)
    test_soundscape_generation(token)
    test_reading_analytics(token)
    test_reading_patterns(token)
    test_create_sample_book()
    
    print("\n🎉 All revolutionary tests completed!")
    print("SensaBook is ready to change the world of reading! 📚✨")

if __name__ == "__main__":
    main() 
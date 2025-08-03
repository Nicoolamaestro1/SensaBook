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
    
    print("\n🎉 All revolutionary tests completed!")
    print("SensaBook is ready to change the world of reading! 📚✨")

if __name__ == "__main__":
    main() 
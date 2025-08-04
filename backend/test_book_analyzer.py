"""
Test script for the new book analyzer functionality.
This demonstrates how to create a book with automatic sound mapping analysis.
"""

import requests
import json

def test_create_book_with_sound_mappings():
    """Test creating a book with automatic sound mapping analysis"""
    
    # Sample Dracula content
    book_data = {
        "title": "Dracula",
        "author": "Bram Stoker",
        "genre": "horror",
        "chapters": [
            {
                "title": "Chapter 1: Jonathan Harker's Journal",
                "pages": [
                    "3 May. Bistritz.—Left Munich at 8:35 P.M., on 1st May, arriving at Vienna early next morning; should have arrived at 6:46, but train was an hour late. Buda-Pesth seems a wonderful place, from the glimpse which I got of it from the train and the little I could walk through the streets. I feared to go very far from the station, as we had arrived late and would start as near the correct time as possible. The impression I had was that we were leaving the West and entering the East; the most western of splendid bridges over the Danube, which is here of noble width and depth, took us among the traditions of Turkish rule.",
                    
                    "We left in pretty good time, and came after nightfall to Klausenburgh. Here I stopped for the night at the Hotel Royale. I had for dinner, or rather supper, a chicken done up some way with red pepper, which was very good but thirsty. (Mem., get recipe for Mina.) I asked the waiter, and he said it was called 'paprika hendl,' and that, as it was a national dish, I should be able to get it anywhere along the Carpathians. I found my smattering of German very useful here; indeed, I don't know how I should be able to get on without it.",
                    
                    "Having had some time at my disposal when in London, I had visited the British Museum, and made search among the books and maps in the library regarding Transylvania; it had struck me that some foreknowledge of the country could hardly fail to have some importance in dealing with a nobleman of that country. I find that the district he named is in the extreme east of the country, just on the borders of three states, Transylvania, Moldavia, and Bukovina, in the midst of the Carpathian mountains; one of the wildest and least known portions of Europe."
                ]
            },
            {
                "title": "Chapter 2: The Castle",
                "pages": [
                    "5 May. The Castle.—The gray of the morning has passed, and the sun is high over the distant horizon, which seems jagged, whether with trees or hills I know not, for it is so far off that big things and little are mixed. I am not sleepy, and, as I am not to be called till I awake, naturally I write till sleep comes. There are many odd things to put down, and, lest who reads them may fancy that I dined too well before I left Bistritz, let me put down my dinner exactly. I dined on what they called 'robber steak'—bits of bacon, onion, and beef, seasoned with red pepper, and strung on sticks and roasted over the fire, in the simple style of the London cat's meat! The wine was Golden Mediasch, which produces a queer sting on the tongue, which is, however, not disagreeable.",
                    
                    "I had to hurry breakfast, for the train started a little before eight, or rather it ought to have done so, for after rushing to the station at 7:30 I had to sit in the carriage for more than an hour before we began to move. It seems to me that the further east you go the more unpunctual are the trains. What ought they to be in China? All day long we seemed to dawdle through a country which was full of beauty of every kind. Sometimes we saw little towns or castles on the top of steep hills such as we see in old missals; sometimes we ran by rivers and streams which seemed from the wide stony margin on each side of them to be subject to great floods. It takes a lot of water, and running strong, to sweep the outside edge of a river clear."
                ]
            }
        ]
    }
    
    # Make the API call
    try:
        response = requests.post(
            "http://localhost:8000/api/books/with-sound-mappings",
            json=book_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Book created successfully!")
            print(f"Book ID: {result['book_id']}")
            print(f"Title: {result['title']}")
            print(f"Author: {result['author']}")
            print(f"Genre: {result['genre']}")
            print(f"Scene mappings: {len(result['scene_mappings'])}")
            print(f"Word mappings: {len(result['word_mappings'])}")
            
            print("\n📊 Scene Mappings:")
            for scene, mapping in result['scene_mappings'].items():
                print(f"  - {scene}: {mapping['sound_file']} (priority: {mapping['priority']})")
            
            print("\n🔊 Word Mappings:")
            for word, sound in result['word_mappings'].items():
                print(f"  - {word}: {sound}")
                
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Error making request: {e}")

def test_soundscape_generation():
    """Test generating soundscape for a specific page"""
    
    try:
        # Get soundscape for the first page of the newly created book
        response = requests.get("http://localhost:8000/soundscape/book/11/chapter1/page/1")
        
        if response.status_code == 200:
            result = response.json()
            print("\n🎵 Soundscape for page 1:")
            print(f"Carpet tracks: {result['carpet_tracks']}")
            print(f"Triggered sounds: {len(result['triggered_sounds'])}")
            
            for sound in result['triggered_sounds']:
                print(f"  - {sound['word']}: {sound['sound']}")
        else:
            print(f"❌ Error getting soundscape: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error testing soundscape: {e}")

if __name__ == "__main__":
    print("🧪 Testing Book Analyzer with Sound Mappings")
    print("=" * 50)
    
    # Test 1: Create book with automatic sound mappings
    test_create_book_with_sound_mappings()
    
    # Test 2: Generate soundscape for a page
    test_soundscape_generation()
    
    print("\n🎉 Test completed!") 
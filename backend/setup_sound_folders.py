#!/usr/bin/env python3
"""
Script to create the comprehensive sound folder structure for triggers.
"""

import os
import shutil

def create_sound_folders():
    """Create all the trigger sound folders"""
    
    # Base path
    base_path = "mobile/app/sounds/triggers"
    
    # All trigger folders we need
    trigger_folders = [
        # Weather & Atmospheric
        "wind",
        "thunder", 
        "water",
        "storm",
        
        # Fire & Heat
        "fire",
        
        # Movement & Transport
        "footsteps",
        "horse",
        "carriage",
        
        # Combat & Weapons
        "sword",
        "armor", 
        "battle",
        
        # Magic & Supernatural
        "magic",
        "supernatural",
        
        # Animals & Creatures
        "birds",
        "wolves",
        "animals",
        
        # Human Sounds
        "human_voices",
        "human_body",
        
        # Mechanical & Objects
        "doors",
        "bells",
        "books",
        
        # Environmental
        "forest",
        "cave",
        "castle"
    ]
    
    print("🎵 Creating sound trigger folders...")
    
    # Create each folder
    for folder in trigger_folders:
        folder_path = os.path.join(base_path, folder)
        
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            print(f"✅ Created: {folder_path}")
        else:
            print(f"📁 Already exists: {folder_path}")
    
    # Move existing files to appropriate folders
    existing_files = {
        "wind.mp3": "wind",
        "storm.mp3": "storm", 
        "footsteps-approaching-316715.mp3": "footsteps"
    }
    
    print("\n📦 Moving existing files to appropriate folders...")
    
    for filename, target_folder in existing_files.items():
        source_path = os.path.join(base_path, filename)
        target_path = os.path.join(base_path, target_folder, filename)
        
        if os.path.exists(source_path):
            if not os.path.exists(target_path):
                shutil.move(source_path, target_path)
                print(f"✅ Moved {filename} → {target_folder}/")
            else:
                print(f"⚠️  {target_folder}/{filename} already exists, keeping original")
        else:
            print(f"❌ Source file not found: {filename}")
    
    print("\n🎯 Sound folder structure created successfully!")
    print("📝 Next steps:")
    print("   1. Add multiple sound files to each folder")
    print("   2. Use descriptive names (e.g., wind_light.mp3, wind_strong.mp3)")
    print("   3. The system will randomly select from each folder")

if __name__ == "__main__":
    create_sound_folders() 
#!/usr/bin/env python3
"""
Script to automatically create sound folders based on TRIGGER_PATTERNS in emotion_analysis.py.
This script reads the TRIGGER_PATTERNS dictionary and creates the corresponding folders.
"""

import os
import re
import ast
from pathlib import Path

def extract_trigger_folders():
    """
    Extract folder names from TRIGGER_PATTERNS in emotion_analysis.py
    """
    # Path to the emotion analysis file
    emotion_file = "app/services/emotion_analysis.py"
    
    try:
        with open(emotion_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find the TRIGGER_PATTERNS dictionary
        pattern_start = content.find("TRIGGER_PATTERNS = {")
        if pattern_start == -1:
            print("❌ TRIGGER_PATTERNS not found in emotion_analysis.py")
            return []
        
        # Find the end of the dictionary
        brace_count = 0
        pattern_end = pattern_start
        
        for i, char in enumerate(content[pattern_start:], pattern_start):
            if char == '{':
                brace_count += 1
            elif char == '}':
                brace_count -= 1
                if brace_count == 0:
                    pattern_end = i + 1
                    break
        
        # Extract the dictionary string
        patterns_dict_str = content[pattern_start:pattern_end]
        
        # Use regex to find all "sound_folder" values
        folder_pattern = r'"sound_folder":\s*"([^"]+)"'
        folders = re.findall(folder_pattern, patterns_dict_str)
        
        # Remove "triggers/" prefix and get unique folders
        unique_folders = list(set([folder.replace("triggers/", "") for folder in folders]))
        
        return unique_folders
        
    except Exception as e:
        print(f"❌ Error reading emotion_analysis.py: {e}")
        return []

def create_sound_folders():
    """
    Create sound folders based on TRIGGER_PATTERNS
    """
    print("🎵 Syncing sound folders with TRIGGER_PATTERNS...")
    
    # Extract folder names from the code
    folders = extract_trigger_folders()
    
    if not folders:
        print("❌ No folders found in TRIGGER_PATTERNS")
        return
    
    # Base path for triggers
    base_path = Path("../mobile/app/sounds/triggers")
    
    print(f"📁 Creating folders in: {base_path}")
    print(f"�� Found {len(folders)} folders to create:")
    
    created_count = 0
    existing_count = 0
    
    for folder in sorted(folders):
        folder_path = base_path / folder
        
        try:
            folder_path.mkdir(parents=True, exist_ok=True)
            
            if folder_path.exists():
                if any(folder_path.iterdir()):
                    print(f"📁 {folder} (exists with files)")
                    existing_count += 1
                else:
                    print(f"✅ {folder} (created)")
                    created_count += 1
            else:
                print(f"✅ {folder} (created)")
                created_count += 1
                
        except Exception as e:
            print(f"❌ Error creating {folder}: {e}")
    
    print(f"\n🎯 Summary:")
    print(f"   ✅ Created: {created_count} folders")
    print(f"   📁 Existing: {existing_count} folders")
    print(f"   📂 Total: {len(folders)} folders")
    
    # Show which folders were found
    print(f"\n📋 Folders from TRIGGER_PATTERNS:")
    for folder in sorted(folders):
        print(f"   • {folder}")

def move_existing_files():
    """
    Move existing sound files to appropriate folders
    """
    print("\n📦 Moving existing files to appropriate folders...")
    
    base_path = Path("../mobile/app/sounds/triggers")
    
    # Map of existing files to their target folders
    file_mapping = {
        "wind.mp3": "wind",
        "storm.mp3": "storm",
        "footsteps-approaching-316715.mp3": "footsteps"
    }
    
    moved_count = 0
    
    for filename, target_folder in file_mapping.items():
        source_path = base_path / filename
        target_path = base_path / target_folder / filename
        
        if source_path.exists():
            if not target_path.exists():
                try:
                    source_path.rename(target_path)
                    print(f"✅ Moved {filename} → {target_folder}/")
                    moved_count += 1
                except Exception as e:
                    print(f"❌ Error moving {filename}: {e}")
            else:
                print(f"⚠️  {target_folder}/{filename} already exists")
        else:
            print(f"❌ Source file not found: {filename}")
    
    print(f"�� Moved {moved_count} files")

def main():
    """
    Main function to sync sound folders
    """
    print("🎵 Sound Folder Sync Tool")
    print("=" * 40)
    
    # Create folders based on TRIGGER_PATTERNS
    create_sound_folders()
    
    # Move existing files
    move_existing_files()
    
    print("\n🎯 Sync complete!")
    print("📝 Next steps:")
    print("   1. Add sound files to each folder")
    print("   2. Use descriptive names (e.g., wind_light.mp3)")
    print("   3. The system will randomly select from each folder")
    print("   4. Run this script again when you add new trigger patterns")

if __name__ == "__main__":
    main() 
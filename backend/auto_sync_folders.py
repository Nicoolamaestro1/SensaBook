#!/usr/bin/env python3
"""
Simple script to automatically sync sound folders.
Can be run periodically or as a cron job.
"""

import os
import sys
from pathlib import Path

def auto_sync():
    """
    Automatically sync sound folders based on TRIGGER_PATTERNS
    """
    # Import the sync function
    sys.path.append('.')
    from sync_sound_folders import create_sound_folders, move_existing_files
    
    print("�� Auto-syncing sound folders...")
    
    # Create folders
    create_sound_folders()
    
    # Move files
    move_existing_files()
    
    print("✅ Auto-sync complete!")

if __name__ == "__main__":
    auto_sync()
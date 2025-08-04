"""
Database migration to add sound mapping tables.
Run this script to create the new tables for database-driven sound mappings.
"""

from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Text, ForeignKey, JSON, Float, Boolean
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Create engine
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_sound_mapping_tables():
    """Create the new sound mapping tables"""
    metadata = MetaData()
    
    # Create book_sound_mappings table
    book_sound_mappings = Table(
        'book_sound_mappings',
        metadata,
        Column('id', Integer, primary_key=True, index=True),
        Column('book_id', Integer, ForeignKey('book.id'), nullable=False),
        Column('mapping_type', String, nullable=False),  # 'scene' or 'word'
        Column('scene_name', String, nullable=True),  # For scene mappings
        Column('keywords', JSON, nullable=False),  # Array of keywords
        Column('sound_file', String, nullable=False),  # MP3 file name
        Column('priority', Integer, default=0),  # Priority for scene mappings
        Column('description', Text, nullable=True)  # Description
    )
    
    # Create sound_files table
    sound_files = Table(
        'sound_files',
        metadata,
        Column('id', Integer, primary_key=True, index=True),
        Column('filename', String, unique=True, nullable=False),
        Column('description', Text, nullable=True),
        Column('category', String, nullable=True),  # 'ambient', 'effect', 'music'
        Column('duration', Float, nullable=True),  # Duration in seconds
        Column('file_size', Integer, nullable=True),  # File size in bytes
        Column('is_available', Boolean, default=True)  # Whether file exists
    )
    
    # Create the tables
    metadata.create_all(bind=engine)
    print("✅ Sound mapping tables created successfully!")

def seed_dracula_mappings():
    """Seed the database with Dracula sound mappings"""
    from app.models.sound_mapping import BookSoundMapping
    from app.services.soundscape_db import create_dracula_sound_mappings
    
    db = SessionLocal()
    try:
        result = create_dracula_sound_mappings(db)
        print(f"✅ {result['message']}")
    except Exception as e:
        print(f"❌ Error seeding Dracula mappings: {e}")
    finally:
        db.close()

def seed_basic_sound_files():
    """Seed the database with basic sound file records"""
    from app.models.sound_mapping import SoundFile
    
    basic_sound_files = [
        {
            "filename": "gothic_castle_ambience.mp3",
            "description": "Dark, echoing castle atmosphere with distant moans",
            "category": "ambient",
            "is_available": False
        },
        {
            "filename": "night_ambience.mp3",
            "description": "Quiet night sounds with occasional owl hoots",
            "category": "ambient",
            "is_available": False
        },
        {
            "filename": "storm_ambience.mp3",
            "description": "Thunder, rain, and wind combined",
            "category": "ambient",
            "is_available": False
        },
        {
            "filename": "wolf_howls.mp3",
            "description": "Distant wolf pack howling",
            "category": "ambient",
            "is_available": False
        },
        {
            "filename": "vampire_hiss.mp3",
            "description": "Dracula's menacing hiss",
            "category": "effect",
            "is_available": False
        },
        {
            "filename": "blood_drip.mp3",
            "description": "Dripping blood sound",
            "category": "effect",
            "is_available": False
        },
        {
            "filename": "thunder_roll.mp3",
            "description": "Deep thunder rumble",
            "category": "effect",
            "is_available": False
        },
        {
            "filename": "wolf_howl.mp3",
            "description": "Single wolf howl",
            "category": "effect",
            "is_available": False
        },
        {
            "filename": "footsteps_stone.mp3",
            "description": "Footsteps on stone floors",
            "category": "effect",
            "is_available": False
        },
        {
            "filename": "door_creak.mp3",
            "description": "Old door creaking open",
            "category": "effect",
            "is_available": False
        }
    ]
    
    db = SessionLocal()
    try:
        for sound_file_data in basic_sound_files:
            # Check if sound file already exists
            existing = db.query(SoundFile).filter(SoundFile.filename == sound_file_data["filename"]).first()
            if not existing:
                db_sound_file = SoundFile(**sound_file_data)
                db.add(db_sound_file)
        
        db.commit()
        print(f"✅ Added {len(basic_sound_files)} basic sound file records")
    except Exception as e:
        print(f"❌ Error seeding sound files: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    print("🚀 Starting sound mapping migration...")
    
    # Step 1: Create tables
    create_sound_mapping_tables()
    
    # Step 2: Seed basic sound files
    seed_basic_sound_files()
    
    # Step 3: Seed Dracula mappings
    seed_dracula_mappings()
    
    print("🎉 Migration completed successfully!") 
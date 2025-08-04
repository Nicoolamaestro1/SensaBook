"""
Database migration to add sound mapping columns to the book table.
Run this script to add the new columns for storing sound mappings with each book.
"""

from sqlalchemy import create_engine, MetaData, Table, Column, JSON, Integer, String, Text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.inspection import inspect
from sqlalchemy.sql import text
from app.core.config import settings

# Create engine
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def add_sound_mapping_columns():
    """Add sound mapping columns to the book table"""
    metadata = MetaData()
    
    # Define the book table with new columns
    book_table = Table(
        'book',
        metadata,
        Column('id', Integer, primary_key=True, index=True),
        Column('title', String, nullable=False),
        Column('author', String, nullable=True),
        Column('summary', Text, nullable=True),
        Column('cover_url', String, nullable=True),
        Column('genre', String, nullable=True),
        # New columns for sound mappings
        Column('scene_mappings', JSON, nullable=True),
        Column('word_mappings', JSON, nullable=True)
    )
    
    # Add the new columns
    with engine.begin() as conn:
        # Check if columns already exist
        inspector = inspect(engine)
        existing_columns = [col['name'] for col in inspector.get_columns('book')]
        
        if 'scene_mappings' not in existing_columns:
            conn.execute(text("ALTER TABLE book ADD COLUMN scene_mappings JSON"))
            print("✅ Added scene_mappings column")
        
        if 'word_mappings' not in existing_columns:
            conn.execute(text("ALTER TABLE book ADD COLUMN word_mappings JSON"))
            print("✅ Added word_mappings column")
    
    print("✅ Sound mapping columns added successfully!")

def analyze_existing_books():
    """Analyze existing books and generate sound mappings for them"""
    from app.services.book_analyzer import BookAnalyzer
    from app.models.book import Book
    
    analyzer = BookAnalyzer()
    db = SessionLocal()
    
    try:
        # Get all books that don't have sound mappings yet
        books = db.query(Book).filter(
            (Book.scene_mappings.is_(None)) | (Book.word_mappings.is_(None))
        ).all()
        
        for book in books:
            print(f"Analyzing book: {book.title}")
            
            # Analyze the book content
            scene_mappings, word_mappings = analyzer.analyze_book_content(book, db)
            
            # Update the book with the mappings
            book.scene_mappings = scene_mappings
            book.word_mappings = word_mappings
            
            print(f"  - Generated {len(scene_mappings)} scene mappings")
            print(f"  - Generated {len(word_mappings)} word mappings")
        
        db.commit()
        print(f"✅ Analyzed {len(books)} existing books")
        
    except Exception as e:
        print(f"❌ Error analyzing existing books: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    print("🚀 Starting book sound mapping migration...")
    
    # Step 1: Add new columns
    add_sound_mapping_columns()
    
    # Step 2: Analyze existing books
    analyze_existing_books()
    
    print("🎉 Migration completed successfully!") 
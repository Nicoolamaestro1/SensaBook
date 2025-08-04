from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.session import get_db
from app.models.sound_mapping import BookSoundMapping, SoundFile
from app.schemas.sound_mapping import (
    SoundMapping, SoundMappingCreate, SoundMappingUpdate,
    BookSoundMappings, SoundFile as SoundFileSchema, SoundFileCreate
)
from app.services.soundscape import get_ambient_soundscape

router = APIRouter()

@router.get("/sound-mappings/book/{book_id}", response_model=BookSoundMappings)
def get_book_sound_mappings(book_id: int, db: Session = Depends(get_db)):
    """Get all sound mappings for a specific book"""
    mappings = db.query(BookSoundMapping).filter(BookSoundMapping.book_id == book_id).all()
    
    scene_mappings = [m for m in mappings if m.mapping_type == 'scene']
    word_mappings = [m for m in mappings if m.mapping_type == 'word']
    
    return BookSoundMappings(
        book_id=book_id,
        scene_mappings=scene_mappings,
        word_mappings=word_mappings
    )

@router.post("/sound-mappings", response_model=SoundMapping)
def create_sound_mapping(mapping: SoundMappingCreate, db: Session = Depends(get_db)):
    """Create a new sound mapping"""
    db_mapping = BookSoundMapping(**mapping.dict())
    db.add(db_mapping)
    db.commit()
    db.refresh(db_mapping)
    return db_mapping

@router.put("/sound-mappings/{mapping_id}", response_model=SoundMapping)
def update_sound_mapping(
    mapping_id: int, 
    mapping_update: SoundMappingUpdate, 
    db: Session = Depends(get_db)
):
    """Update an existing sound mapping"""
    db_mapping = db.query(BookSoundMapping).filter(BookSoundMapping.id == mapping_id).first()
    if not db_mapping:
        raise HTTPException(status_code=404, detail="Sound mapping not found")
    
    update_data = mapping_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_mapping, field, value)
    
    db.commit()
    db.refresh(db_mapping)
    return db_mapping

@router.delete("/sound-mappings/{mapping_id}")
def delete_sound_mapping(mapping_id: int, db: Session = Depends(get_db)):
    """Delete a sound mapping"""
    db_mapping = db.query(BookSoundMapping).filter(BookSoundMapping.id == mapping_id).first()
    if not db_mapping:
        raise HTTPException(status_code=404, detail="Sound mapping not found")
    
    db.delete(db_mapping)
    db.commit()
    return {"message": "Sound mapping deleted successfully"}

@router.post("/sound-mappings/bulk", response_model=List[SoundMapping])
def create_bulk_sound_mappings(mappings: List[SoundMappingCreate], db: Session = Depends(get_db)):
    """Create multiple sound mappings at once"""
    db_mappings = []
    for mapping in mappings:
        db_mapping = BookSoundMapping(**mapping.dict())
        db.add(db_mapping)
        db_mappings.append(db_mapping)
    
    db.commit()
    for mapping in db_mappings:
        db.refresh(mapping)
    
    return db_mappings

@router.get("/sound-files", response_model=List[SoundFileSchema])
def get_sound_files(
    category: Optional[str] = Query(None, description="Filter by category"),
    available_only: bool = Query(True, description="Show only available files"),
    db: Session = Depends(get_db)
):
    """Get available sound files"""
    query = db.query(SoundFile)
    
    if category:
        query = query.filter(SoundFile.category == category)
    
    if available_only:
        query = query.filter(SoundFile.is_available == True)
    
    return query.all()

@router.post("/sound-files", response_model=SoundFileSchema)
def create_sound_file(sound_file: SoundFileCreate, db: Session = Depends(get_db)):
    """Register a new sound file"""
    db_sound_file = SoundFile(**sound_file.dict())
    db.add(db_sound_file)
    db.commit()
    db.refresh(db_sound_file)
    return db_sound_file

@router.get("/soundscape/book/{book_id}/chapter/{chapter_number}/page/{page_number}")
def get_soundscape_with_db_mappings(
    book_id: int, 
    chapter_number: int, 
    page_number: int, 
    db: Session = Depends(get_db)
):
    """Get soundscape using database mappings instead of hardcoded ones"""
    # This will use the new database-driven sound mapping system
    return get_ambient_soundscape(book_id, chapter_number, page_number, db) 
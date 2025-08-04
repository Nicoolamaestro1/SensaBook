from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class SoundMappingBase(BaseModel):
    mapping_type: str  # 'scene' or 'word'
    scene_name: Optional[str] = None
    keywords: List[str]
    sound_file: str
    priority: int = 0
    description: Optional[str] = None

class SoundMappingCreate(SoundMappingBase):
    book_id: int

class SoundMappingUpdate(BaseModel):
    mapping_type: Optional[str] = None
    scene_name: Optional[str] = None
    keywords: Optional[List[str]] = None
    sound_file: Optional[str] = None
    priority: Optional[int] = None
    description: Optional[str] = None

class SoundMapping(SoundMappingBase):
    id: int
    book_id: int

    class Config:
        from_attributes = True

class BookSoundMappings(BaseModel):
    book_id: int
    scene_mappings: List[SoundMapping]
    word_mappings: List[SoundMapping]

class SoundFileBase(BaseModel):
    filename: str
    description: Optional[str] = None
    category: Optional[str] = None
    duration: Optional[float] = None
    file_size: Optional[int] = None
    is_available: bool = True

class SoundFileCreate(SoundFileBase):
    pass

class SoundFile(SoundFileBase):
    id: int

    class Config:
        from_attributes = True

class SoundscapeResponse(BaseModel):
    book_id: int
    chapter_id: int
    page_id: int
    summary: str
    detected_scenes: List[str]
    scene_keyword_counts: Dict[str, int]
    scene_keyword_positions: Dict[str, List[int]]
    carpet_tracks: List[str]
    triggered_sounds: List[Dict[str, Any]] 
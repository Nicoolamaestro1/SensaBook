# Database-Driven Sound Mappings

## 🎯 Overview

This feature replaces hardcoded Python sound mappings with a flexible, database-driven system that allows dynamic sound configuration per book.

## 🚀 Benefits

### ✅ **Dynamic & Flexible**
- Add new books without touching code
- Modify sound mappings per book
- A/B test different sound combinations
- User-customizable sound preferences

### ✅ **Scalable**
- No code changes needed for new books
- Easy to manage hundreds of books
- Version control for sound mappings
- Backup/restore sound configurations

### ✅ **User-Friendly**
- Authors/publishers can create their own sound maps
- Users can customize their reading experience
- Admin interface for managing mappings
- Real-time updates without deployments

## 🗄️ Database Schema

### `book_sound_mappings` Table
```sql
CREATE TABLE book_sound_mappings (
    id INTEGER PRIMARY KEY,
    book_id INTEGER REFERENCES book(id),
    mapping_type VARCHAR NOT NULL, -- 'scene' or 'word'
    scene_name VARCHAR, -- For scene mappings
    keywords JSON NOT NULL, -- Array of keywords
    sound_file VARCHAR NOT NULL, -- MP3 file name
    priority INTEGER DEFAULT 0, -- Priority for scene mappings
    description TEXT -- Description of the sound effect
);
```

### `sound_files` Table
```sql
CREATE TABLE sound_files (
    id INTEGER PRIMARY KEY,
    filename VARCHAR UNIQUE NOT NULL,
    description TEXT,
    category VARCHAR, -- 'ambient', 'effect', 'music'
    duration FLOAT, -- Duration in seconds
    file_size INTEGER, -- File size in bytes
    is_available BOOLEAN DEFAULT TRUE
);
```

## 📡 API Endpoints

### Sound Mappings
- `GET /api/sound-mappings/book/{book_id}` - Get all mappings for a book
- `POST /api/sound-mappings` - Create a new mapping
- `PUT /api/sound-mappings/{mapping_id}` - Update a mapping
- `DELETE /api/sound-mappings/{mapping_id}` - Delete a mapping
- `POST /api/sound-mappings/bulk` - Create multiple mappings

### Sound Files
- `GET /api/sound-files` - Get available sound files
- `POST /api/sound-files` - Register a new sound file

### Soundscape (Database-Driven)
- `GET /api/soundscape/book/{book_id}/chapter/{chapter}/page/{page}` - Get soundscape using DB mappings

## 🎵 Example: Dracula Sound Mappings

### Scene Mappings (Atmosphere)
```json
{
  "book_id": 10,
  "mapping_type": "scene",
  "scene_name": "dracula_castle",
  "keywords": ["castle", "dracula", "count", "vampire", "tomb", "grave", "coffin", "undead", "blood", "throat"],
  "sound_file": "gothic_castle_ambience.mp3",
  "priority": 5,
  "description": "Dark, echoing castle atmosphere"
}
```

### Word Mappings (Trigger Effects)
```json
{
  "book_id": 10,
  "mapping_type": "word",
  "keywords": ["dracula", "vampire"],
  "sound_file": "vampire_hiss.mp3",
  "priority": 1,
  "description": "Dracula's menacing hiss"
}
```

## 🔧 Setup Instructions

### 1. Run Migration
```bash
cd backend
python migrations/add_sound_mappings.py
```

### 2. Test the API
```bash
# Get Dracula sound mappings
curl http://localhost:8000/api/sound-mappings/book/10

# Create a new mapping
curl -X POST http://localhost:8000/api/sound-mappings \
  -H "Content-Type: application/json" \
  -d '{
    "book_id": 10,
    "mapping_type": "word",
    "keywords": ["moon"],
    "sound_file": "moon_howl.mp3",
    "description": "Mysterious moon sound"
  }'
```

### 3. Test Soundscape
```bash
# Get soundscape for Dracula page 1
curl http://localhost:8000/api/soundscape/book/10/chapter/1/page/1
```

## 🎨 Frontend Integration

The mobile app will automatically use the database-driven soundscape endpoint when available. The system falls back to the legacy hardcoded mappings if no database mappings exist.

## 🔄 Migration Strategy

1. **Phase 1**: Deploy database schema and API endpoints
2. **Phase 2**: Migrate existing books to database mappings
3. **Phase 3**: Update frontend to use new endpoints
4. **Phase 4**: Remove legacy hardcoded mappings

## 🛠️ Development

### Adding New Books
1. Create sound mappings via API
2. Upload sound files to mobile app
3. Test with real book content
4. Iterate and refine mappings

### Customizing Mappings
- Use the API to modify existing mappings
- A/B test different keyword sets
- Adjust priorities for better scene detection
- Add new sound files as needed

## 🎯 Future Enhancements

- **AI-Powered Mapping**: Use NLP to automatically suggest mappings
- **User Preferences**: Allow users to customize their sound experience
- **Community Mappings**: Share and rate sound mappings
- **Real-Time Updates**: WebSocket updates for live mapping changes
- **Analytics**: Track which sounds are most effective
- **Machine Learning**: Learn from user behavior to improve mappings

## 🐛 Troubleshooting

### Common Issues
1. **No sounds playing**: Check if mappings exist for the book
2. **Wrong sounds**: Verify keyword matching logic
3. **Missing files**: Ensure sound files are uploaded to mobile app
4. **Performance**: Optimize database queries for large mapping sets

### Debug Commands
```bash
# Check if mappings exist
curl http://localhost:8000/api/sound-mappings/book/10

# Test soundscape generation
curl http://localhost:8000/api/soundscape/book/10/chapter/1/page/1

# Check sound files
curl http://localhost:8000/api/sound-files
``` 
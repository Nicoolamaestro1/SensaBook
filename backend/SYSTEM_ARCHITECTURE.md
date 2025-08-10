# SensaBook Soundscape System Architecture

## Overview
The SensaBook soundscape system is a sophisticated audio engine that analyzes book content and generates immersive soundscapes in real-time. It operates on three distinct layers, each providing different levels of audio sophistication.

## System Layers

### Layer 1: Simple Trigger Words
**Purpose**: Immediate sound effects for specific words
**Implementation**: `find_trigger_words()` in `emotion_analysis.py`
**Function**: Detects individual words like "thunder", "fire", "sword" and triggers immediate sound effects
**Timing**: Calculates precise timing based on reading speed (words per minute)

**Key Functions**:
- `find_trigger_words(text: str)` - Main trigger detection
- `calculateWordTiming()` - Determines when to play sounds
- `SoundManager.playTrigger()` - Plays immediate sound effects

### Layer 2: Enhanced Scene Detection
**Purpose**: Complex pattern recognition for broader narrative contexts
**Implementation**: `enhanced_scene_detection()` in `soundscape.py`
**Function**: Uses sophisticated regex patterns to detect scenes like "epic battle", "mystical magic", "romantic love"
**Output**: Scene classification with mood, weight, and audio recommendations

**Scene Types**:
- `epic_battle` - Heroic combat scenes
- `mystical_magic` - Magical and supernatural elements
- `romantic_love` - Romantic and emotional moments
- `dark_evil` - Dark and ominous scenes
- `mountain_journey` - Adventure and travel sequences
- `storm_weather` - Atmospheric weather conditions

### Layer 3: Psychoacoustic Analysis
**Purpose**: Advanced audio engineering optimization
**Implementation**: Psychoacoustic metadata in scene mappings
**Function**: Provides detailed audio parameters for optimal sound mixing

**Parameters**:
- `frequency_range` - Low, mid, high frequency balance
- `spatial_width` - Stero field positioning (wide, narrow, intimate)
- `temporal_dynamics` - How sounds evolve over time
- `emotional_curve` - Emotional progression patterns
- `volume_profile` - Dynamic volume control
- `reverb_type` - Environmental acoustic characteristics

## Data Flow

### 1. Book Opening
```
BookDetailScreen mounts → useBook() fetches book data → paginateText() breaks content into pages
```

### 2. Content Analysis
```
findTriggerWords() → Layer 1 detection → loadSoundscapeForPage() → API call to backend
```

### 3. Backend Processing
```
get_soundscape() endpoint → get_ambient_soundscape() → enhanced_scene_detection() → Layer 2+3 analysis
```

### 4. Sound Generation
```
Return soundscape data → Mobile app processes → SoundManager plays appropriate sounds
```

## Key Components

### Frontend (React Native)
- `BookDetailScreen` - Main reading interface
- `SoundManager` - Audio playback controller
- `findTriggerWords()` - Local trigger detection
- `loadSoundscapeForPage()` - Backend API integration

### Backend (Python/FastAPI)
- `soundscape.py` - Core soundscape logic
- `emotion_analysis.py` - Trigger word detection
- `enhanced_scene_detection()` - Complex scene analysis
- `get_ambient_soundscape()` - Orchestrates all layers

### Audio Assets
- **Trigger Sounds**: Immediate effects (thunder, sword, footsteps)
- **Carpet Tracks**: Background ambience (storm, forest, cabin)
- **Psychoacoustic Profiles**: Audio engineering metadata

## Integration Points

### API Endpoints
```
GET /soundscape/book/{book_id}/chapter{chapter_number}/page/{page_number}
```

### Data Structures
```python
# Soundscape Response
{
    "detected_scenes": List[str],
    "carpet_tracks": List[str], 
    "triggered_sounds": List[Dict],
    "mood_analysis": Dict,
    "psychoacoustic_profile": Dict
}
```

## Performance Considerations

### Caching
- Scene detection results cached per page
- Trigger word positions calculated once per page
- Audio assets preloaded for immediate playback

### Optimization
- Regex patterns optimized for speed
- Psychoacoustic calculations batched
- Audio mixing handled by native audio engine

## Future Enhancements

### Planned Features
- Machine learning-based emotion detection
- Dynamic soundscape adaptation
- User preference learning
- Multi-language support
- Accessibility features (audio descriptions)

### Scalability
- Microservice architecture for audio processing
- CDN integration for audio assets
- Real-time collaboration features
- Cloud-based audio generation

## Troubleshooting

### Common Issues
1. **No sounds playing**: Check audio permissions and volume
2. **API errors**: Verify backend is running on port 8000
3. **Trigger detection**: Ensure text contains recognized trigger words
4. **Scene detection**: Check regex patterns in `ENHANCED_SCENE_SOUND_MAPPINGS`

### Debug Mode
Enable detailed logging in `soundscape.py` and `emotion_analysis.py` for troubleshooting.

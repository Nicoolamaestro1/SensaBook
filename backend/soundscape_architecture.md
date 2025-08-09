# Soundscape System Architecture

## Overview
The soundscape system consists of 4 main services that work together to analyze text and generate appropriate sounds:

1. **soundscape.py** - Main orchestrator and API interface
2. **page_analyzer.py** - Combines mood and emotion analysis
3. **mood_analyzer.py** - Analyzes atmospheric mood for carpet sounds
4. **emotion_analysis.py** - Detects trigger words and emotional content

## Service Relationships

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Frontend      │───▶│   soundscape.py  │───▶│ page_analyzer.py│
│   Request       │    │   (Main API)     │    │ (Combines both) │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │                        │
                                ▼                        ▼
                       ┌──────────────────┐    ┌─────────────────┐
                       │ mood_analyzer.py │    │emotion_analysis.py│
                       │ (Carpet Sounds) │    │ (Trigger Words) │
                       └──────────────────┘    └─────────────────┘
```

## Detailed Flow

### 1. Frontend Request
```typescript
// Frontend calls:
GET /soundscape/book/4/chapter1/page/1
```

### 2. soundscape.py (Main Orchestrator)
**Purpose**: Main API endpoint that coordinates everything

**Key Functions**:
- `get_ambient_soundscape()` - Main function called by API
- `advanced_scene_detection()` - Detects scenes using SCENE_SOUND_MAPPINGS
- `detect_triggered_sounds()` - Calls emotion_analysis for trigger words

**SCENE_SOUND_MAPPINGS**:
```python
SCENE_SOUND_MAPPINGS = {
    "mountains": {
        "keywords": ["mountains", "cliff", "peak", "valley"],
        "carpet": "ambience/windy_mountains.mp3"
    },
    "indoors": {
        "keywords": ["cabin", "indoors", "house", "room"],
        "carpet": "ambience/cabin.mp3"
    }
    # ... more scenes
}
```

**Flow**:
1. Gets book page content from database
2. Calls `advanced_scene_detection()` for carpet sounds
3. Calls `detect_triggered_sounds()` for trigger words
4. Returns combined result

### 3. page_analyzer.py (Combiner)
**Purpose**: Combines mood analysis and emotion analysis into one service

**Key Functions**:
- `analyze_page_complete()` - Main analysis function
- `get_soundscape_recommendation()` - Formats output for frontend

**Flow**:
1. Calls `mood_analyzer.analyze_page_mood()` for carpet sounds
2. Calls `emotion_analysis.find_trigger_words()` for trigger words
3. Combines results and calculates confidence
4. Returns unified soundscape recommendation

### 4. mood_analyzer.py (Carpet Sounds)
**Purpose**: Analyzes text mood to suggest background ambient sounds

**Key Functions**:
- `analyze_page_mood()` - Main mood analysis
- `_suggest_sound()` - Maps mood to sound file

**MOOD_CATEGORIES**:
```python
MOOD_CATEGORIES = {
    "peaceful": {
        "keywords": ["peace", "calm", "quiet", "gentle"],
        "sounds": ["ambience/default_ambience", "ambience/cabin"],
        "description": "Calm, comfortable, safe atmosphere"
    },
    "epic": {
        "keywords": ["epic", "heroic", "battle", "war"],
        "sounds": ["ambience/storm", "ambience/thunder-city-377703"],
        "description": "Large-scale, heroic, powerful events"
    }
    # ... more moods
}
```

**Analysis Process**:
1. Analyzes geographic elements (mountains, water, indoors)
2. Analyzes weather elements (storm, wind, night)
3. Analyzes emotional intensity
4. Determines primary and secondary moods
5. Suggests appropriate carpet sound

### 5. emotion_analysis.py (Trigger Words)
**Purpose**: Detects specific words that should trigger sound effects

**Key Functions**:
- `find_trigger_words()` - Main trigger word detection
- `AdvancedEmotionAnalyzer` - Advanced emotion analysis (unused in current flow)

**TRIGGER_WORDS**:
```python
TRIGGER_WORDS = {
    "thunder": "ambience/thunder-city-377703",
    "wind": "triggers/wind",
    "footsteps": "triggers/footsteps-approaching-316715",
    "storm": "triggers/storm",
    "fire": "triggers/storm",
    # ... many more
}
```

**Analysis Process**:
1. Scans text for trigger words
2. Calculates timing based on word position
3. Returns list of trigger words with timing and sound files

## Complete Data Flow Example

### Input Text:
```
"The mountains were covered in snow and thunder echoed through the valley. 
Frodo sat quietly by the stream, listening to the peaceful sounds of nature."
```

### 1. soundscape.py Processing:
```python
# Scene Detection
detected_scenes = ["mountains", "indoors"]  # From SCENE_SOUND_MAPPINGS
carpet_sound = "ambience/windy_mountains.mp3"  # Most frequent scene

# Trigger Word Detection (via emotion_analysis.py)
trigger_words = [
    {"word": "thunder", "sound": "ambience/thunder-city-377703", "timing": 2.5},
    {"word": "stream", "sound": "ambience/cabin_rain", "timing": 8.1}
]
```

### 2. page_analyzer.py Processing:
```python
# Mood Analysis (via mood_analyzer.py)
mood_result = {
    "primary_mood": "peaceful",
    "suggested_sound": "ambience/cabin"
}

# Combined Result
final_result = {
    "carpet_tracks": ["ambience/windy_mountains.mp3"],
    "triggered_sounds": [
        {"word": "thunder", "sound": "ambience/thunder-city-377703", "timing": 2.5},
        {"word": "stream", "sound": "ambience/cabin_rain", "timing": 8.1}
    ],
    "mood": "peaceful",
    "confidence": 0.85
}
```

### 3. Frontend Receives:
```json
{
    "carpet_tracks": ["ambience/windy_mountains.mp3"],
    "triggered_sounds": [...],
    "mood": "peaceful",
    "confidence": 0.85,
    "detected_scenes": ["mountains", "indoors"],
    "summary": "Scenes: mountains(1), indoors(1); Triggers: thunder, stream"
}
```

## Current Usage

**Currently Active Flow**:
```
Frontend → soundscape.py → SCENE_SOUND_MAPPINGS (carpet) + emotion_analysis.py (triggers)
```

**Alternative Flow** (via page_analyzer.py):
```
Frontend → soundscape.py → page_analyzer.py → mood_analyzer.py (carpet) + emotion_analysis.py (triggers)
```

## Key Differences

### soundscape.py (Current Primary):
- Uses **SCENE_SOUND_MAPPINGS** for carpet sounds
- Direct keyword matching
- Simple, reliable, predictable
- **Currently active in production**

### page_analyzer.py (Alternative):
- Uses **mood_analyzer.py** for carpet sounds
- More sophisticated mood analysis
- Better for complex emotional content
- **Available but not currently primary**

## Why This Architecture?

1. **Separation of Concerns**: Each service has a specific responsibility
2. **Modularity**: Easy to swap or improve individual components
3. **Reliability**: Multiple analysis methods available
4. **Flexibility**: Can use different approaches for different needs

## Current Status

✅ **soundscape.py** - Active and working perfectly
✅ **emotion_analysis.py** - Active for trigger words
✅ **mood_analyzer.py** - Available for advanced mood analysis
✅ **page_analyzer.py** - Available for combined analysis

The system is robust and provides multiple analysis approaches while maintaining the reliable SCENE_SOUND_MAPPINGS for carpet sounds. 
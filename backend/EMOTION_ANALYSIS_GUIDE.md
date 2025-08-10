# Emotion Analysis & Soundscape Integration Guide

## Overview
The emotion analysis system is the core intelligence behind SensaBook's soundscape generation. It analyzes text content to detect emotions, themes, and trigger words, then maps these to appropriate audio experiences.

## Core Components

### 1. AdvancedEmotionAnalyzer Class
**Location**: `backend/app/services/emotion_analysis.py`
**Purpose**: Main analyzer that processes text and generates soundscape recommendations

**Key Methods**:
```python
class AdvancedEmotionAnalyzer:
    def analyze_emotions(self, text: str) -> EmotionResult
    def analyze_themes(self, text: str) -> ThemeResult  
    def analyze_emotional_progression(self, text: str) -> EmotionalProgressionResult
    def generate_soundscape_recommendations(self, emotion_result, theme_result) -> Dict
```

### 2. Emotion Detection
**Supported Emotions**:
- `JOY` - Happiness, excitement, delight
- `SADNESS` - Grief, melancholy, sorrow
- `ANGER` - Rage, fury, irritation
- `FEAR` - Terror, anxiety, dread
- `SURPRISE` - Shock, amazement, astonishment
- `DISGUST` - Revulsion, repulsion, sickness
- `NEUTRAL` - Balanced, calm, indifferent

**Detection Method**: Keyword-based analysis with intensity scoring

### 3. Theme Detection
**Supported Themes**:
- `ADVENTURE` - Quest, journey, exploration
- `ROMANCE` - Love, passion, affection
- `MYSTERY` - Investigation, secrets, clues
- `HORROR` - Terror, nightmare, supernatural
- `FANTASY` - Magic, wizardry, mythical creatures
- `DRAMA` - Conflict, tension, betrayal

**Detection Method**: Contextual phrase analysis with confidence scoring

## Trigger Word System (Layer 1)

### Implementation
**Function**: `find_trigger_words(text: str) -> List[Dict]`
**Purpose**: Detects specific words that should trigger immediate sound effects

### Trigger Patterns
```python
TRIGGER_PATTERNS = {
    "thunder": {
        "sound": "triggers/thunder.mp3",
        "priority": "high",
        "folder": "thunder"
    },
    "fire": {
        "sound": "triggers/fire.mp3", 
        "priority": "medium",
        "folder": "fire"
    },
    "sword": {
        "sound": "triggers/sword.mp3",
        "priority": "high",
        "folder": "sword"
    }
    # ... more patterns
}
```

### Timing Calculation
```python
def calculateWordTiming(text: str, wpm: number = 120):
    words = text.split(/\s+/).filter(Boolean)
    msPerWord = 60_000 / wpm  # 60 seconds / words per minute
    return { words, msPerWord }
```

### Output Structure
```python
{
    "word": "thunder",
    "sound": "triggers/thunder.mp3",
    "position": 15,
    "timing": 7500,  # milliseconds
    "priority": "high"
}
```

## Emotional Progression Analysis

### EmotionalProgressionResult
```python
@dataclass
class EmotionalProgressionResult:
    segments: List[Dict]           # Text segments with emotions
    progression_patterns: List[str] # Emotional arc patterns
    arc_metrics: Dict              # Quantitative emotional measures
    overall_trend: str             # Overall emotional direction
```

### Analysis Process
1. **Text Segmentation**: Breaks text into manageable chunks
2. **Emotion Mapping**: Assigns emotions to each segment
3. **Pattern Recognition**: Identifies emotional progression patterns
4. **Arc Calculation**: Measures emotional intensity and direction
5. **Trend Analysis**: Determines overall emotional trajectory

## Integration with Soundscape System

### 1. Frontend Integration
```typescript
// mobile/app/book/[bookId].tsx
const findTriggerWords = (text: string) => {
  // Local trigger detection for immediate response
  const found: TriggerWord[] = [];
  // ... detection logic
  return found;
};

const loadSoundscapeForPage = async () => {
  // Backend API call for complex analysis
  const response = await fetch(`/soundscape/book/${bookId}/...`);
  const data = await response.json();
  // Process soundscape data
};
```

### 2. Backend Integration
```python
# backend/app/services/soundscape.py
def get_ambient_soundscape(book_id, chapter_number, page_number, db):
    # Get trigger words (Layer 1)
    trigger_words = detect_triggered_sounds(book_page.content)
    
    # Get complex scenes (Layer 2)
    sorted_scenes, scene_counts, scene_positions, mood_analysis = enhanced_scene_detection(book_page.content)
    
    # Return complete soundscape data
    return {
        "triggered_sounds": trigger_words,
        "detected_scenes": sorted_scenes,
        "mood_analysis": mood_analysis
    }
```

### 3. Data Flow
```
Text Input → Emotion Analysis → Trigger Detection → Scene Detection → Soundscape Generation
    ↓              ↓                ↓                ↓                ↓
EmotionResult → TriggerWords → ScenePatterns → AudioMetadata → FinalSoundscape
```

## Soundscape Mapping

### Emotion → Sound Mapping
```python
def _map_emotion_to_soundscape(self, emotion: EmotionType) -> str:
    emotion_soundscapes = {
        EmotionType.JOY: "bright_ambience.mp3",
        EmotionType.SADNESS: "melancholy_drones.mp3", 
        EmotionType.ANGER: "tense_rhythms.mp3",
        EmotionType.FEAR: "dark_ambience.mp3",
        EmotionType.SURPRISE: "sudden_impact.mp3",
        EmotionType.DISGUST: "unsettling_tones.mp3",
        EmotionType.NEUTRAL: "default_ambience.mp3"
    }
    return emotion_soundscapes.get(emotion, "default_ambience.mp3")
```

### Theme → Sound Mapping
```python
def _map_theme_to_soundscape(self, theme: ThemeType) -> str:
    theme_soundscapes = {
        ThemeType.ADVENTURE: "epic_journey.mp3",
        ThemeType.ROMANCE: "romantic_melody.mp3",
        ThemeType.MYSTERY: "mysterious_ambience.mp3",
        ThemeType.HORROR: "horror_ambience.mp3",
        ThemeType.FANTASY: "magical_atmosphere.mp3",
        ThemeType.DRAMA: "tension_buildup.mp3"
    }
    return theme_soundscapes.get(theme, "default_ambience.mp3")
```

## Performance & Optimization

### Caching Strategy
- **Emotion Results**: Cached per text chunk
- **Theme Analysis**: Cached per page
- **Trigger Words**: Cached per page with timing
- **Soundscape Data**: Cached per page

### Optimization Techniques
- **Keyword Indexing**: Fast emotion/theme lookup
- **Pattern Precompilation**: Regex patterns compiled once
- **Batch Processing**: Multiple analyses processed together
- **Lazy Loading**: Audio assets loaded on demand

## Testing & Debugging

### Test Cases
```python
# Test emotion detection
analyzer = AdvancedEmotionAnalyzer()
result = analyzer.analyze_emotions("The hero felt overwhelming joy")
assert result.primary_emotion == EmotionType.JOY
assert result.intensity > 0.7

# Test trigger detection
triggers = find_trigger_words("Thunder crashed overhead")
assert len(triggers) > 0
assert triggers[0]["word"] == "thunder"
```

### Debug Mode
Enable detailed logging to see:
- Emotion detection process
- Theme analysis steps
- Trigger word matching
- Soundscape generation decisions

## Future Enhancements

### Machine Learning Integration
- **BERT-based emotion detection** for more nuanced analysis
- **Sentiment analysis** for emotional intensity
- **Context-aware** emotion detection
- **Multi-language** emotion support

### Advanced Features
- **Emotional memory** across reading sessions
- **Personalized** soundscape preferences
- **Adaptive** emotional thresholds
- **Real-time** emotion tracking

## Troubleshooting

### Common Issues
1. **No emotions detected**: Check text content and emotion keywords
2. **Trigger words not working**: Verify TRIGGER_PATTERNS configuration
3. **Slow performance**: Check caching and optimization settings
4. **Audio not playing**: Verify sound file paths and permissions

### Debug Commands
```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Test specific components
analyzer = AdvancedEmotionAnalyzer()
result = analyzer.analyze_emotions("test text")
print(f"Debug result: {result}")
```

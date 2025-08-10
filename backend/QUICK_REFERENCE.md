# SensaBook Quick Reference Guide

## 🚀 **Essential Functions & Their Purposes**

### **Backend Core Functions**

#### **Soundscape Generation**
```python
# Main soundscape orchestrator
get_ambient_soundscape(book_id, chapter_number, page_number, db)
# → Returns complete soundscape data for a page

# Complex scene detection (Layer 2)
enhanced_scene_detection(text)
# → Detects narrative scenes using regex patterns

# Simple trigger detection (Layer 1)  
detect_triggered_sounds(text)
# → Finds individual trigger words like "thunder", "sword"
```

#### **Emotion Analysis**
```python
# Main emotion analyzer
AdvancedEmotionAnalyzer.analyze_emotions(text)
# → Returns EmotionResult with primary emotion and intensity

# Theme detection
AdvancedEmotionAnalyzer.analyze_themes(text)  
# → Returns ThemeResult with detected themes

# Emotional progression
AdvancedEmotionAnalyzer.analyze_emotional_progression(text)
# → Returns EmotionalProgressionResult with emotional arc
```

#### **API Endpoints**
```python
# Soundscape endpoint
GET /soundscape/book/{book_id}/chapter{chapter_number}/page/{page_number}
# → Returns soundscape data for mobile app
```

### **Mobile App Functions**

#### **Book Reading**
```typescript
// Main reading screen
BookDetailScreen
// → Handles book display, pagination, and soundscape integration

// Text pagination
paginateText(content: string)
// → Breaks book content into readable pages

// Trigger word detection (client-side)
findTriggerWords(text: string)
// → Local detection for immediate response
```

#### **Sound Management**
```typescript
// Audio playback controller
SoundManager.playTrigger(sound: string)
// → Plays immediate sound effects

SoundManager.playCarpet(sound: string)  
// → Plays background ambience

// Soundscape loading
loadSoundscapeForPage(chapterIndex: number, pageIndex: number)
// → Fetches soundscape data from backend
```

#### **Reading Timer**
```typescript
// Word-by-word timing
calculateWordTiming()
// → Determines when to play trigger sounds

// Timer control
startReadingTimer()
stopReadingTimer()
// → Manages reading progress and sound timing
```

## 🔧 **Key Data Structures**

### **Soundscape Response**
```python
{
    "detected_scenes": List[str],           # ["epic_battle", "mystical_magic"]
    "carpet_tracks": List[str],             # ["storm_ambience.mp3", "forest.mp3"]
    "triggered_sounds": List[Dict],         # Trigger word data
    "mood_analysis": Dict,                  # Emotional analysis results
    "psychoacoustic_profile": Dict          # Audio engineering metadata
}
```

### **Trigger Word Data**
```python
{
    "word": "thunder",
    "sound": "triggers/thunder.mp3", 
    "position": 15,
    "timing": 7500,  # milliseconds
    "priority": "high"
}
```

### **Scene Detection Result**
```python
(
    sorted_scenes,      # List of detected scene types
    scene_counts,       # Count of each scene type
    scene_positions,    # Position of scenes in text
    mood_analysis      # Emotional progression data
)
```

## 📁 **Critical File Locations**

### **Backend**
- `app/services/soundscape.py` - Core soundscape logic
- `app/services/emotion_analysis.py` - Emotion and theme analysis
- `app/api/soundscape.py` - Soundscape API endpoint
- `app/main.py` - FastAPI application entry point

### **Mobile**
- `app/book/[bookId].tsx` - Main reading interface
- `utils/soundManager.ts` - Audio playback controller
- `services/api.ts` - Backend API integration
- `app/_layout.tsx` - App navigation structure

### **Configuration**
- `requirements.txt` - Python dependencies
- `package.json` - Node.js dependencies
- `docker-compose.yml` - Docker setup
- `.env` - Environment variables (create from env.example)

## ⚡ **Quick Start Commands**

### **Backend**
```bash
cd backend
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### **Mobile**
```bash
cd mobile
npm install
npm start
```

### **Database**
```bash
docker-compose up -d
```

## 🎯 **Common Development Tasks**

### **Add New Trigger Word**
1. Add to `TRIGGER_PATTERNS` in `emotion_analysis.py`
2. Add audio file to `mobile/app/sounds/triggers/`
3. Test with `find_trigger_words()`

### **Add New Scene Type**
1. Add pattern to `ENHANCED_SCENE_SOUND_MAPPINGS` in `soundscape.py`
2. Define regex pattern, weight, mood, and psychoacoustic metadata
3. Test with `enhanced_scene_detection()`

### **Modify Audio Behavior**
1. Update `SoundManager` methods in `mobile/utils/soundManager.ts`
2. Adjust timing in `calculateWordTiming()`
3. Test audio playback on device

### **Debug API Issues**
1. Check backend logs: `uvicorn --log-level debug`
2. Test endpoint directly: `curl http://localhost:8000/soundscape/...`
3. Use FastAPI docs: `http://localhost:8000/docs`

## 🚨 **Troubleshooting Quick Fixes**

### **No Sounds Playing**
- Check device volume and permissions
- Verify audio file paths exist
- Ensure SoundManager is initialized

### **API Connection Failed**
- Verify backend is running on port 8000
- Check network configuration
- Ensure CORS is properly set

### **Scene Detection Not Working**
- Check regex patterns in `ENHANCED_SCENE_SOUND_MAPPINGS`
- Verify text contains expected patterns
- Test with simple text first

### **Performance Issues**
- Check database query performance
- Optimize regex patterns
- Implement caching for repeated requests

## 📚 **Key Concepts to Remember**

1. **Three-Layer System**: Simple triggers → Complex scenes → Psychoacoustic optimization
2. **Real-time Processing**: Text analysis happens as you read, not pre-generated
3. **Audio Synchronization**: Sounds are timed to word positions, not just page loads
4. **Context Awareness**: Scene detection considers surrounding text, not just individual words
5. **Mobile-First**: Designed for mobile reading with optimized audio playback

## 🔄 **Development Workflow**

1. **Make Changes** → Edit relevant files
2. **Test Locally** → Run backend and mobile separately
3. **Debug Issues** → Use logging and console output
4. **Commit Changes** → Use descriptive commit messages
5. **Test Integration** → Verify frontend-backend communication

## 📞 **When You Need Help**

1. **Check Logs** - Backend and mobile console output
2. **Test Components** - Isolate the issue to specific functions
3. **Verify Data** - Check API responses and data structures
4. **Review Documentation** - Check these markdown files
5. **Ask Questions** - Be specific about what's not working

---

**Remember**: The system is designed to be modular. If one part isn't working, the others should still function. Start with simple trigger words, then work up to complex scene detection.

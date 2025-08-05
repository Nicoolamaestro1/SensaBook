# Soundscape Usage Guide: When Each Approach is Used

## 🎯 **Current vs Alternative Usage**

The system has **two different approaches** for generating soundscapes, and they're used in **different contexts**:

## 📊 **Current Approach (Primary - Always Used)**

### **When Used**: 
- **ALL frontend requests** for soundscape data
- **Main API endpoint**: `/soundscape/book/{id}/chapter{num}/page/{num}`
- **Used by**: Mobile app, web app, any client requesting soundscape

### **How It Works**:
```python
# soundscape.py - Main orchestrator
def get_ambient_soundscape(book_id, chapter_number, page_number, db):
    # 1. Gets page content from database
    # 2. Uses SCENE_SOUND_MAPPINGS for carpet sounds
    # 3. Uses emotion_analysis.py for trigger words
    # 4. Returns combined result
```

### **Flow**:
```
Frontend Request → soundscape.py → SCENE_SOUND_MAPPINGS + emotion_analysis.py
```

### **Example API Call**:
```typescript
// Frontend calls this:
GET /soundscape/book/4/chapter1/page/1
```

### **Response**:
```json
{
    "carpet_tracks": ["ambience/windy_mountains.mp3"],
    "triggered_sounds": [...],
    "detected_scenes": ["mountains", "travel", "storm"],
    "summary": "Scenes: mountains(3), travel(1), storm(1); Triggers: war, mountain..."
}
```

---

## 🔬 **Alternative Approach (Analytics/Testing Only)**

### **When Used**:
- **Analytics endpoints** for detailed analysis
- **Testing and debugging** soundscape generation
- **Advanced mood analysis** when needed
- **NOT used by frontend** for regular soundscape requests

### **How It Works**:
```python
# page_analyzer.py - Combines mood and emotion analysis
def analyze_page_complete(text):
    # 1. Calls mood_analyzer.py for carpet sounds
    # 2. Calls emotion_analysis.py for trigger words
    # 3. Combines with confidence scores
    # 4. Returns sophisticated analysis
```

### **Flow**:
```
Analytics Request → page_analyzer.py → mood_analyzer.py + emotion_analysis.py
```

### **Example API Calls**:
```typescript
// Analytics endpoints (NOT used by frontend):
POST /api/analytics/analyze-page
GET /api/analytics/analyze-book-page/{book_id}/{chapter_number}/{page_number}
POST /api/analytics/analyze-text-batch
```

### **Response**:
```json
{
    "carpet_sound": "ambience/windy_mountains",
    "trigger_words": [...],
    "primary_mood": "journey",
    "confidence": 1.0,
    "reasoning": "Atmosphere: journey (Primary mood: journey...)"
}
```

---

## 🎯 **Key Differences**

| Aspect | Current (soundscape.py) | Alternative (page_analyzer.py) |
|--------|------------------------|-------------------------------|
| **Usage** | ✅ **Production - Frontend** | 🔬 **Analytics/Testing** |
| **Carpet Sounds** | SCENE_SOUND_MAPPINGS | mood_analyzer.py |
| **Complexity** | Simple, reliable | Sophisticated, advanced |
| **Predictability** | High | Variable |
| **Performance** | Fast | Slower (more analysis) |
| **API Endpoint** | `/soundscape/book/{id}/...` | `/api/analytics/...` |

---

## 🔄 **When Each is Used**

### **Current Approach (soundscape.py) - ALWAYS for Frontend**
```typescript
// This is what your mobile app calls:
fetch('http://localhost:8000/soundscape/book/4/chapter1/page/1')
```

**Used for**:
- ✅ Mobile app soundscape requests
- ✅ Web app soundscape requests  
- ✅ Any client requesting soundscape data
- ✅ Production soundscape generation

### **Alternative Approach (page_analyzer.py) - Analytics Only**
```typescript
// These are for analytics/testing:
fetch('http://localhost:8000/api/analytics/analyze-page', {
    method: 'POST',
    body: JSON.stringify({ text: "sample text" })
})
```

**Used for**:
- 🔬 Detailed mood analysis
- 🔬 Testing different analysis methods
- 🔬 Debugging soundscape generation
- 🔬 Advanced analytics features

---

## 🎵 **Real Example**

### **Frontend Request (Current)**:
```typescript
// Mobile app calls this:
const response = await fetch('/soundscape/book/4/chapter1/page/1');
const data = await response.json();
// data.carpet_tracks = ["ambience/windy_mountains.mp3"]
// data.triggered_sounds = [...]
```

### **Analytics Request (Alternative)**:
```typescript
// Analytics/testing calls this:
const response = await fetch('/api/analytics/analyze-page', {
    method: 'POST',
    body: JSON.stringify({ text: "The mountains were..." })
});
const data = await response.json();
// data.primary_mood = "journey"
// data.confidence = 1.0
```

---

## 🚀 **Current Status**

### **✅ Production (Frontend)**:
- **soundscape.py** - Active and working perfectly
- **emotion_analysis.py** - Active for trigger words
- **SCENE_SOUND_MAPPINGS** - Active for carpet sounds

### **🔬 Analytics (Testing)**:
- **page_analyzer.py** - Available for advanced analysis
- **mood_analyzer.py** - Available for mood analysis
- **Advanced features** - Available for testing

---

## 🎯 **Summary**

**For your mobile app**: Always uses the **Current Approach** (soundscape.py)
**For analytics/testing**: Uses the **Alternative Approach** (page_analyzer.py)

The system is designed so that:
1. **Frontend gets reliable, fast soundscapes** via soundscape.py
2. **Analytics get sophisticated analysis** via page_analyzer.py
3. **Both approaches are available** for different needs

**Your mobile app will always get the reliable SCENE_SOUND_MAPPINGS approach!** 🎉 
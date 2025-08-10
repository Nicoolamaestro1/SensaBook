# SensaBook Development Workflow Guide

## Overview
This guide explains how to work with the SensaBook codebase, including development setup, testing procedures, and deployment workflows.

## Project Structure

### Backend (Python/FastAPI)
```
backend/
├── app/
│   ├── api/           # API endpoints and routing
│   ├── core/          # Configuration and core settings
│   ├── db/            # Database models and sessions
│   ├── models/        # Data models
│   ├── schemas/       # Pydantic schemas
│   ├── services/      # Business logic (soundscape, emotion analysis)
│   └── main.py        # FastAPI application entry point
├── requirements.txt   # Python dependencies
├── Dockerfile         # Container configuration
└── README.md          # Backend-specific documentation
```

### Mobile (React Native/Expo)
```
mobile/
├── app/               # App screens and navigation
├── components/        # Reusable UI components
├── services/          # API service calls
├── utils/             # Utility functions (SoundManager)
├── assets/            # Images, fonts, and audio files
├── package.json       # Node.js dependencies
└── app.json          # Expo configuration
```

## Development Setup

### 1. Backend Setup
```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp env.example .env
# Edit .env with your configuration

# Start development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Mobile Setup
```bash
# Navigate to mobile directory
cd mobile

# Install Node.js dependencies
npm install

# Start Expo development server
npm start
# or
expo start
```

### 3. Database Setup
```bash
# Using Docker (recommended)
docker-compose up -d

# Or manually install PostgreSQL and configure connection
```

## Development Workflow

### 1. Feature Development
```bash
# Create feature branch
git checkout -b feature/soundscape-enhancement

# Make changes to code
# Test locally

# Commit changes
git add .
git commit -m "feat: enhance soundscape detection patterns"

# Push and create pull request
git push origin feature/soundscape-enhancement
```

### 2. Testing Strategy

#### Backend Testing
```python
# Run all tests
pytest

# Run specific test file
pytest tests/test_soundscape.py

# Run with coverage
pytest --cov=app tests/

# Run specific test function
pytest tests/test_soundscape.py::test_enhanced_scene_detection
```

#### Mobile Testing
```bash
# Run on iOS simulator
npm run ios

# Run on Android emulator
npm run android

# Run on web
npm run web

# Run tests
npm test
```

### 3. Code Quality

#### Python (Backend)
```bash
# Format code
black app/
isort app/

# Lint code
flake8 app/
mypy app/

# Pre-commit hooks (if configured)
pre-commit run --all-files
```

#### TypeScript/JavaScript (Mobile)
```bash
# Format code
npx prettier --write .

# Lint code
npm run lint

# Type checking
npx tsc --noEmit
```

## Key Development Areas

### 1. Soundscape System
**Location**: `backend/app/services/soundscape.py`

**Key Functions**:
- `enhanced_scene_detection()` - Complex scene pattern recognition
- `get_ambient_soundscape()` - Main soundscape generation
- `detect_triggered_sounds()` - Simple trigger word detection

**Development Notes**:
- Scene patterns are defined in `ENHANCED_SCENE_SOUND_MAPPINGS`
- Psychoacoustic metadata provides advanced audio parameters
- Context rules refine scene detection accuracy

### 2. Emotion Analysis
**Location**: `backend/app/services/emotion_analysis.py`

**Key Classes**:
- `AdvancedEmotionAnalyzer` - Main analysis engine
- `EmotionResult` - Emotion detection results
- `ThemeResult` - Theme analysis results

**Development Notes**:
- Emotion keywords are configurable in the class
- Theme detection uses contextual phrase analysis
- Integration with soundscape system is seamless

### 3. Mobile App
**Location**: `mobile/app/book/[bookId].tsx`

**Key Components**:
- `BookDetailScreen` - Main reading interface
- `SoundManager` - Audio playback controller
- `findTriggerWords()` - Local trigger detection

**Development Notes**:
- Uses Expo Router for navigation
- Audio playback handled by Expo AV
- Real-time soundscape integration with backend

## API Development

### 1. Adding New Endpoints
```python
# backend/app/api/endpoints/new_feature.py
from fastapi import APIRouter, Depends
from app.services.new_service import new_function
from app.db.session import get_db

router = APIRouter(prefix="/new-feature", tags=["New Feature"])

@router.get("/")
def get_new_feature(db: Session = Depends(get_db)):
    """New feature endpoint"""
    return new_function(db)
```

### 2. Service Layer
```python
# backend/app/services/new_service.py
from app.db.session import get_db
from app.models.book import Book

def new_function(db: Session) -> Dict:
    """Business logic for new feature"""
    # Implementation here
    return {"result": "success"}
```

### 3. Database Models
```python
# backend/app/models/new_model.py
from sqlalchemy import Column, Integer, String
from app.db.base_class import Base

class NewModel(Base):
    __tablename__ = "new_models"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
```

## Testing Guidelines

### 1. Unit Tests
```python
# tests/test_new_service.py
import pytest
from app.services.new_service import new_function

def test_new_function():
    """Test new function behavior"""
    result = new_function()
    assert result["result"] == "success"
```

### 2. Integration Tests
```python
# tests/test_api.py
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_new_endpoint():
    """Test new API endpoint"""
    response = client.get("/new-feature/")
    assert response.status_code == 200
    assert response.json()["result"] == "success"
```

### 3. Mobile Tests
```typescript
// mobile/__tests__/BookDetailScreen.test.tsx
import { render, screen } from '@testing-library/react-native';
import BookDetailScreen from '../app/book/[bookId]';

test('renders book content', () => {
  render(<BookDetailScreen />);
  expect(screen.getByText('Book Content')).toBeInTheDocument();
});
```

## Debugging

### 1. Backend Debugging
```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Add debug prints
print(f"Debug: {variable}")

# Use Python debugger
import pdb; pdb.set_trace()
```

### 2. Mobile Debugging
```typescript
// Console logging
console.log('Debug:', variable);

// React Native Debugger
// Install and use React Native Debugger for advanced debugging

// Expo DevTools
// Use Expo DevTools for real-time debugging
```

### 3. API Debugging
```bash
# Test endpoints directly
curl http://localhost:8000/soundscape/book/1/chapter1/page/1

# Use FastAPI automatic docs
# Visit http://localhost:8000/docs
```

## Performance Optimization

### 1. Backend
- **Caching**: Implement Redis for frequently accessed data
- **Database**: Optimize queries and add indexes
- **Async**: Use async/await for I/O operations
- **Compression**: Enable gzip compression

### 2. Mobile
- **Image Optimization**: Compress and resize images
- **Lazy Loading**: Load components on demand
- **Memory Management**: Proper cleanup of audio resources
- **Bundle Optimization**: Tree shaking and code splitting

## Deployment

### 1. Backend Deployment
```bash
# Build Docker image
docker build -t sensabook-backend .

# Run container
docker run -p 8000:8000 sensabook-backend

# Or use docker-compose
docker-compose up --build
```

### 2. Mobile Deployment
```bash
# Build for production
expo build:android
expo build:ios

# Or use EAS Build
eas build --platform all
```

## Monitoring & Logging

### 1. Application Logs
```python
# Structured logging
import structlog
logger = structlog.get_logger()

logger.info("Soundscape generated", 
           book_id=book_id, 
           scenes=len(detected_scenes))
```

### 2. Performance Monitoring
```python
# Add timing to functions
import time

def timed_function():
    start_time = time.time()
    result = do_work()
    duration = time.time() - start_time
    logger.info("Function completed", duration=duration)
    return result
```

## Common Issues & Solutions

### 1. Audio Not Playing
- Check device permissions
- Verify audio file paths
- Ensure SoundManager is properly initialized
- Check volume settings

### 2. API Connection Errors
- Verify backend is running on correct port
- Check network configuration
- Ensure CORS is properly configured
- Verify API endpoint paths

### 3. Performance Issues
- Check database query performance
- Monitor memory usage
- Optimize regex patterns
- Implement proper caching

## Contributing Guidelines

### 1. Code Style
- Follow existing code patterns
- Use descriptive variable names
- Add type hints (Python) and types (TypeScript)
- Write clear docstrings and comments

### 2. Testing
- Write tests for new features
- Ensure all tests pass before committing
- Maintain good test coverage
- Test edge cases and error conditions

### 3. Documentation
- Update relevant documentation files
- Add inline comments for complex logic
- Document API changes
- Update README files as needed

## Resources

### Documentation
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Native Documentation](https://reactnative.dev/)
- [Expo Documentation](https://docs.expo.dev/)

### Tools
- [Postman](https://www.postman.com/) - API testing
- [React Native Debugger](https://github.com/jhen0409/react-native-debugger)
- [Expo DevTools](https://docs.expo.dev/guides/debugging/)

### Community
- [FastAPI Discord](https://discord.gg/VQjKpNj)
- [React Native Community](https://github.com/react-native-community)
- [Expo Community](https://forums.expo.dev/)

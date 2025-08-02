# SensaBook Backend API

**Revolutionary Immersive Reading Platform Backend**

This is the core backend API for SensaBook, an immersive book reading platform that uses AI-powered emotion analysis to create dynamic soundscapes that adapt to the mood and content of your reading experience.

## 🚀 Revolutionary Features

### **AI-Powered Emotion Analysis**
- Real-time sentiment analysis of book content
- Advanced NLP using spaCy for emotion detection
- Theme and atmosphere analysis
- Dynamic soundscape generation based on text mood

### **Immersive Audio Experience**
- Contextual soundscape recommendations
- Emotion-based audio intensity adjustment
- Theme-specific sound effects
- Adaptive volume control

### **Personalized Reading Analytics**
- Reading speed tracking and analysis
- Emotional engagement measurement
- Personalized book recommendations
- Reading pattern insights

### **Advanced User Management**
- JWT-based authentication
- User preferences and reading goals
- Reading statistics and streaks
- Social reading features

## 🏗️ Architecture

```
backend/
├── app/
│   ├── api/                    # API endpoints
│   │   ├── auth.py            # Authentication endpoints
│   │   ├── endpoints/
│   │   │   ├── books.py       # Book management
│   │   │   └── analytics.py   # Analytics & emotion analysis
│   │   └── router.py          # Main router
│   ├── core/                  # Core configuration
│   │   ├── config.py          # Settings management
│   │   └── security.py        # JWT & password handling
│   ├── db/                    # Database layer
│   │   └── session.py         # Database session management
│   ├── models/                # SQLAlchemy models
│   │   ├── book.py           # Book, Chapter, Page models
│   │   └── user.py           # User model
│   ├── schemas/               # Pydantic schemas
│   │   └── user.py           # User schemas
│   ├── services/              # Business logic
│   │   ├── emotion_analysis.py    # AI emotion analysis
│   │   ├── reading_analytics.py   # Reading analytics
│   │   └── soundscape.py          # Soundscape generation
│   └── main.py               # FastAPI application
└── requirements.txt           # Dependencies
```

## 🛠️ Setup & Installation

### Prerequisites
- Python 3.8+
- PostgreSQL
- Redis (optional, for caching)

### Installation

1. **Clone and navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install spaCy model:**
   ```bash
   python -m spacy download en_core_web_sm
   ```

5. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials
   ```

6. **Run the server:**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

## 📚 API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login user
- `GET /auth/me` - Get current user profile
- `PUT /auth/me` - Update user profile
- `GET /auth/me/preferences` - Get user preferences
- `PUT /auth/me/preferences` - Update user preferences
- `GET /auth/me/stats` - Get reading statistics

### Book Management
- `GET /api/books` - Get all books
- `GET /api/books/{book_id}` - Get specific book
- `POST /api/book` - Create new book

### Revolutionary Analytics & Emotion Analysis
- `POST /api/analytics/analyze-emotion` - Analyze text emotion
- `POST /api/analytics/analyze-theme` - Analyze text theme
- `POST /api/analytics/generate-soundscape` - Generate soundscape recommendations
- `GET /api/analytics/book/{book_id}/page/{chapter}/{page}/soundscape` - Get page soundscape
- `GET /api/analytics/me/stats` - Get user reading stats
- `GET /api/analytics/me/recommendations` - Get book recommendations
- `GET /api/analytics/me/patterns` - Analyze reading patterns
- `POST /api/analytics/track-session` - Track reading session
- `GET /api/analytics/books/{book_id}/emotion-analysis` - Analyze book emotions

## 🔧 Configuration

### Environment Variables
```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/sensabook

# JWT
SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Redis (optional)
REDIS_URL=redis://localhost:6379

# AI Models
SPACY_MODEL=en_core_web_sm
EMOTION_ANALYSIS_ENABLED=true
SOUNDSCAPE_GENERATION_ENABLED=true

# Performance
CACHE_ENABLED=true
ANALYTICS_ENABLED=true
```

## 🧠 AI Features

### Emotion Analysis
The system uses advanced NLP to detect emotions in text:
- **Joy**: happy, excited, delighted, thrilled
- **Sadness**: sad, depressed, grief, sorrow
- **Anger**: angry, furious, rage, enraged
- **Fear**: afraid, terrified, scared, horrified
- **Surprise**: surprised, shocked, amazed, astonished
- **Disgust**: disgusted, revolted, repulsed, sickened

### Theme Detection
Identifies themes and settings:
- **Adventure**: quest, journey, explore, discover
- **Romance**: love, heart, kiss, passion
- **Mystery**: mystery, clue, investigate, secret
- **Horror**: horror, terrifying, nightmare, haunted
- **Fantasy**: magic, wizard, spell, dragon
- **Drama**: conflict, tension, struggle, betrayal

### Soundscape Generation
Creates contextual audio recommendations:
- Emotion-based primary soundscapes
- Theme-based secondary soundscapes
- Dynamic volume adjustment
- Contextual sound effects

## 📊 Analytics Features

### Reading Analytics
- **Speed Tracking**: Words per minute calculation
- **Session Analysis**: Reading session categorization
- **Engagement Measurement**: Emotional engagement scoring
- **Pattern Recognition**: Peak reading times, preferences

### Personalization
- **Genre Preferences**: Based on reading history
- **Recommendation Engine**: Personalized book suggestions
- **Reading Goals**: Progress tracking and achievements
- **Social Features**: Reading streaks and sharing

## 🔒 Security

- **JWT Authentication**: Secure token-based authentication
- **Password Hashing**: bcrypt for secure password storage
- **CORS Configuration**: Proper cross-origin resource sharing
- **Input Validation**: Pydantic models for data validation

## 🚀 Performance

- **Database Optimization**: Efficient queries with SQLAlchemy
- **Caching**: Redis integration for performance
- **Async Support**: FastAPI's async capabilities
- **Connection Pooling**: Optimized database connections

## 🧪 Testing

```bash
# Run tests (when implemented)
pytest

# Run with coverage
pytest --cov=app
```

## 📈 Monitoring

- **Health Checks**: `/health` endpoint
- **API Documentation**: Auto-generated with FastAPI
- **Error Logging**: Comprehensive error tracking
- **Performance Metrics**: Response time monitoring

## 🔮 Future Enhancements

- **Real-time Audio Generation**: Dynamic soundscape creation
- **Voice Narration**: Text-to-speech integration
- **Advanced NLP**: More sophisticated emotion analysis
- **Machine Learning**: Personalized recommendation improvements
- **Social Features**: Book clubs and reading groups
- **Mobile Optimization**: Enhanced mobile API support

## 📖 API Documentation

Once the server is running, visit:
- **Interactive API Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**SensaBook Backend** - Revolutionizing the reading experience through AI-powered emotion analysis and immersive audio experiences. 🚀 
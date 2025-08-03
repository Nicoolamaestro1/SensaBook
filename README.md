````markdown name=README.md
# SensaBook

**Immersive Book Reader**  
[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

SensaBook is an immersive book reading platform that enhances your reading experience by blending text with dynamic soundscapes and emotion-aware features. Designed with a modern Python backend and a React Native mobile frontend, it personalizes your literary journey by adapting ambient audio to the mood of each chapter, offering personalized recommendations, and supporting rich user profiles.

---

## Features

- **Book Management:** Add, update, delete, and upload book content and metadata (author, genre, cover image).
- **User Authentication:** Register, login, and manage personalized reading profiles.
- **Emotion Analysis:** Maps book/chapter emotions using NLP to matching soundscapes.
- **Soundscape Generation:** Audio playback synced to reading progress. Adaptive ambient sounds based on story mood.
- **Personalization:** Recommends books and adapts soundscapes to user preferences or mood.
- **Progress Tracking:** Bookmarks and reading history for each user.
- **Mobile UI:** Modern React Native app with Home, Reader, Settings, and Profile screens.
- **API-first Design:** FastAPI backend with documented RESTful endpoints.
- **Testing & Quality:** Unit/integration tests and planned CI/CD pipeline (GitHub Actions).
- **Accessibility:** Focus on readable fonts, color contrast, and easy navigation.

---

## Getting Started

### 🐳 Quick Start with Docker (Recommended)

The easiest way to get started is using Docker:

```bash
# Clone the repository
git clone <repository-url>
cd SensaBook

# Start all services
docker-compose up --build
```

This will start:
- **PostgreSQL Database** on port 5432
- **Backend API** on port 8000  
- **Frontend (Mobile App)** on port 8081

Access the application:
- **Frontend:** http://localhost:8081
- **API Docs:** http://localhost:8000/docs

For detailed Docker setup instructions, see [`DOCKER_SETUP.md`](DOCKER_SETUP.md).

### Manual Setup

#### Backend (Python/FastAPI)
1. **Install dependencies:**
    ```sh
    cd backend
    pip install -r requirements.txt
    ```
2. **Configure environment:**
    - Copy `.env.example` to `.env` and set database credentials.
3. **Run the server:**
    ```sh
    uvicorn app.main:app --reload
    ```

#### Mobile (React Native)
1. **Install dependencies:**
    ```sh
    cd mobile
    npm install
    ```
2. **Start the app:**
    ```sh
    npx expo start --web
    ```

---

## Project Structure

See [`docs/project-structure.md`](docs/project-structure.md) for an in-depth layout.
```
sensa-book/
│
├── backend/               # Python backend (FastAPI)
│   ├── app/
│   │   ├── api/           # Route definitions
│   │   ├── core/          # Config, constants
│   │   ├── models/        # Data models
│   │   ├── services/      # Business logic, AI analysis, sound generation
│   │   ├── db/            # Database access
│   │   └── main.py        # App entry point
│   ├── requirements.txt
│   └── .env
│
├── mobile/                # React Native frontend
│   ├── assets/            # Fonts, images, sounds
│   ├── components/        # UI components
│   ├── screens/           # App screens
│   ├── services/          # API/audio
│   ├── hooks/             # Custom hooks
│   ├── context/           # Global state
│   └── App.tsx
│
├── docs/                  # Diagrams, planning notes
├── ROADMAP.md             # Development plan
├── LICENSE
└── README.md
```

---

## Roadmap Highlights

- Advanced emotion/sentiment analysis with AI/NLP.
- Voice narration (Text-to-Speech).
- Adaptive and personalized recommendations.
- Beta release & feedback collection.
- Accessibility and performance improvements.

See [`ROADMAP.md`](ROADMAP.md) for details.

---

## Contributing

We welcome issues, suggestions, and pull requests!  
- Use GitHub Issues/Projects to track bugs and feature requests.
- Please read the roadmap and project structure docs before contributing.

---

## License

This project is licensed under the MIT License – see the [`LICENSE`](LICENSE) file for details.

---

## Useful Resources

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [React Native Docs](https://reactnative.dev/docs/getting-started)
- [NLP with Python](https://realpython.com/natural-language-processing-spacy-python/)
- [Audio in React Native](https://github.com/react-native-community/react-native-audio-toolkit)
````

# SensaBook
Immersive book reader
sensa-book/
│
├── backend/               # Python backend (FastAPI or Flask recommended)
│   ├── app/
│   │   ├── api/           # Route definitions
│   │   ├── core/          # Settings, config, constants
│   │   ├── models/        # Pydantic or ORM models
│   │   ├── services/      # Business logic, AI analysis, sound generation
│   │   ├── db/            # Database access layer
│   │   └── main.py        # App entry point
│   ├── requirements.txt   # Backend dependencies
│   └── .env               # Secrets and environment config
│
├── mobile/                # React Native frontend
│   ├── assets/            # Fonts, images, sounds
│   ├── components/        # Shared UI components
│   ├── screens/           # App screens (Home, Reader, Settings, etc.)
│   ├── services/          # API service calls, audio handling
│   ├── hooks/             # Custom React hooks
│   ├── context/           # Global state (e.g. theme, audio)
│   ├── App.tsx            # Root component
│   ├── navigation/        # Navigation setup (React Navigation)
│   ├── utils/             # Helper functions
│   └── package.json       # RN dependencies
│
├── docs/                  # Diagrams, planning notes
│
├── README.md
└── .gitignore
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.router import api_router
from .core.config import settings

app = FastAPI(
    title="SensaBook API",
    description="Intelligent reading analytics and soundscape generation",
    version="2.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the new simplified API router
app.include_router(api_router, prefix="/api")

@app.get("/")
async def root():
    return {
        "message": "SensaBook API - Intelligent Soundscape Generation",
        "version": "2.0.0",
        "status": "active",
        "features": [
            "Scene-aware soundscape generation",
            "Genre-aware adjustments",
            "Config-driven patterns",
            "Dracula problem solved"
        ]
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "system": "SensaBook"}








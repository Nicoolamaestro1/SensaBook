from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import router as api_router 
# from app.api.router import router as api_router
from app.db.session import engine, Base
from app.models.book import Book  # Import your models


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow multiple ports
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)
 
Book.metadata.create_all(bind=engine)








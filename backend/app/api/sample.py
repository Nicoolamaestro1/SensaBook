from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User

router = APIRouter()

@router.get("/ping")
async def ping():
    return {"message": "pong"}

@router.get("/users")
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()
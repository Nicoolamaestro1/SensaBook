from sqlalchemy import Column, Integer, String, Text
from app.db.session import Base

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    summary = Column(Text, nullable=True)
    cover_url = Column(String, nullable=True)
    genre = Column(String, nullable=True)
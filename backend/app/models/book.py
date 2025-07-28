from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base

class Book(Base):
    __tablename__ = "book"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=True)
    summary = Column(Text, nullable=True)
    cover_url = Column(String, nullable=True)
    genre = Column(String, nullable=True)

    pages = relationship("BookPage", order_by="BookPage.page_number", back_populates="book")


class BookPage(Base):
    __tablename__ = "book_pages"

    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey("book.id"))
    page_number = Column(Integer, index=True)
    content = Column(Text)

    book = relationship("Book", back_populates="pages")

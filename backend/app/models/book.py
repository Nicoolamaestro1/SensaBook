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

    chapters = relationship("Chapter", order_by="Chapter.chapter_number", back_populates="book")


class Chapter(Base):
    __tablename__ = "chapter"

    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey("book.id"))
    chapter_number = Column(Integer, index=True)
    title = Column(String, nullable=True)

    book = relationship("Book", back_populates="chapters")
    pages = relationship("Page", order_by="Page.page_number", back_populates="chapter")


class Page(Base):
    __tablename__ = "page"

    id = Column(Integer, primary_key=True)
    chapter_id = Column(Integer, ForeignKey("chapter.id"))
    book_id = Column(Integer, ForeignKey("book.id"))
    page_number = Column(Integer, index=True)
    content = Column(Text)

    chapter = relationship("Chapter", back_populates="pages")

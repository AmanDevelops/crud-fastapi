"""Database models for the application."""
from sqlalchemy import Column, String, Integer, Boolean
from app.database import Base


class Review(Base):
    """
        Represents reviews in the database.
    """
    __tablename__ = "reviews"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    is_active = Column(Boolean, default=False)


class User(Base):
    """
        Represents users in the database.
    """
    __tablename__ = "users"
    username = Column(String, unique=True, primary_key=True)
    password = Column(String, nullable=False)

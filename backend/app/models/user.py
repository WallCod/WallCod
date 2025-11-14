"""
User database model.
"""
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, Integer, Text
from sqlalchemy.orm import relationship
from ..core.database import Base


class User(Base):
    """User model for authentication and profile management."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(50), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(100))

    # Profile information
    bio = Column(Text)
    avatar_url = Column(String(500))
    github_url = Column(String(255))
    linkedin_url = Column(String(255))
    twitter_url = Column(String(255))
    website_url = Column(String(255))

    # Skills and experience
    skills = Column(Text)  # JSON array of skills
    job_title = Column(String(100))
    company = Column(String(100))
    location = Column(String(100))

    # Account status
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    is_superuser = Column(Boolean, default=False)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    last_login = Column(DateTime)

    # Relationships
    # projects = relationship("Project", back_populates="user")
    # posts = relationship("BlogPost", back_populates="author")

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"

    @property
    def is_authenticated(self):
        """Check if user is authenticated."""
        return True

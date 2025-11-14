"""
User schemas for request/response validation.
"""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field, validator


class UserBase(BaseModel):
    """Base user schema."""
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50, pattern="^[a-zA-Z0-9_-]+$")
    full_name: Optional[str] = Field(None, max_length=100)


class UserCreate(UserBase):
    """Schema for user registration."""
    password: str = Field(..., min_length=8, max_length=100)

    @validator('password')
    def validate_password(cls, v):
        """Validate password strength."""
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        return v


class UserUpdate(BaseModel):
    """Schema for user profile updates."""
    full_name: Optional[str] = Field(None, max_length=100)
    bio: Optional[str] = Field(None, max_length=500)
    avatar_url: Optional[str] = Field(None, max_length=500)
    github_url: Optional[str] = Field(None, max_length=255)
    linkedin_url: Optional[str] = Field(None, max_length=255)
    twitter_url: Optional[str] = Field(None, max_length=255)
    website_url: Optional[str] = Field(None, max_length=255)
    skills: Optional[List[str]] = None
    job_title: Optional[str] = Field(None, max_length=100)
    company: Optional[str] = Field(None, max_length=100)
    location: Optional[str] = Field(None, max_length=100)


class UserInDB(UserBase):
    """Schema for user in database."""
    id: int
    bio: Optional[str] = None
    avatar_url: Optional[str] = None
    github_url: Optional[str] = None
    linkedin_url: Optional[str] = None
    twitter_url: Optional[str] = None
    website_url: Optional[str] = None
    skills: Optional[str] = None
    job_title: Optional[str] = None
    company: Optional[str] = None
    location: Optional[str] = None
    is_active: bool
    is_verified: bool
    is_superuser: bool
    created_at: datetime
    updated_at: datetime
    last_login: Optional[datetime] = None

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    """Schema for user response."""
    id: int
    email: EmailStr
    username: str
    full_name: Optional[str] = None
    bio: Optional[str] = None
    avatar_url: Optional[str] = None
    github_url: Optional[str] = None
    linkedin_url: Optional[str] = None
    twitter_url: Optional[str] = None
    website_url: Optional[str] = None
    job_title: Optional[str] = None
    company: Optional[str] = None
    location: Optional[str] = None
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    """Schema for JWT token response."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    """Schema for JWT token payload."""
    sub: Optional[str] = None
    exp: Optional[int] = None

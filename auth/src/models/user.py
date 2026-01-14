"""
User Pydantic Models for validation
"""
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional


class UserRegisterInput(BaseModel):
    """Input model for user registration."""
    email: EmailStr
    password: str = Field(min_length=8, max_length=100)


class UserLoginInput(BaseModel):
    """Input model for user login."""
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    """Response model for user data (excludes password)."""
    id: int
    email: str
    createdAt: datetime

    class Config:
        from_attributes = True

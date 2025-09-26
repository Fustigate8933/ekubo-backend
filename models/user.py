"""
User Pydantic schemas for API.
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict, EmailStr


# Pydantic schemas
class UserBase(BaseModel):
    """Base user schema."""
    email: Optional[EmailStr] = None
    username: str = Field(..., min_length=3, max_length=50)


class UserCreate(UserBase):
    """Schema for creating a user."""
    password: str = Field(..., min_length=8, max_length=100)


class UserUpdate(UserBase):
    """Schema for updating a user."""
    password: Optional[str] = Field(None, min_length=8, max_length=100)


class UserResponse(UserBase):
    """Schema for user responses."""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_at: datetime


class UserInDB(UserResponse):
    """Schema for user in database."""
    password: str


class UserLogin(BaseModel):
    """Schema for user login."""
    email: EmailStr
    password: str = Field(..., min_length=8)


class UserSignup(UserCreate):
    """Schema for user signup."""
    pass

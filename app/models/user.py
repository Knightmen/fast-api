from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
from datetime import datetime
from email_validator import validate_email, EmailNotValidError

class UserBase(BaseModel):
    email: str = Field(
        ...,
        description="User's email address",
        examples=["john.doe@example.com"]
    )
    username: str = Field(
        ...,
        min_length=3,
        max_length=50,
        description="Username for login (3-50 characters)",
        examples=["john_doe"]
    )
    full_name: Optional[str] = Field(
        None,
        min_length=1,
        max_length=100,
        description="User's full name",
        examples=["John Doe"]
    )

    @field_validator('email')
    @classmethod
    def validate_email(cls, v: str) -> str:
        if not v:
            raise ValueError("Email address cannot be empty")
        try:
            # Validate and normalize the email
            email_info = validate_email(v, check_deliverability=False)
            normalized_email = email_info.normalized
            return normalized_email
        except EmailNotValidError as e:
            raise ValueError("Invalid email address format. Please provide a valid email (e.g., user@example.com)")

class UserCreate(UserBase):
    password: str = Field(
        ...,
        min_length=8,
        description="Password must be at least 8 characters long",
        examples=["StrongP@ssw0rd"]
    )

class User(UserBase):
    id: int = Field(..., description="Unique user identifier")
    is_active: bool = Field(default=True, description="Whether the user account is active")
    created_at: datetime = Field(..., description="Timestamp when the user was created")

    class Config:
        from_attributes = True 
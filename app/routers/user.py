from fastapi import APIRouter, HTTPException
from typing import List
from datetime import datetime
from ..models.user import User, UserCreate

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

# Simulated database (in memory)
fake_users_db = [
    {
        "id": 1,
        "email": "john@example.com",
        "username": "john_doe",
        "full_name": "John Doe",
        "is_active": True,
        "created_at": datetime.now()
    },
    {
        "id": 2,
        "email": "jane@example.com",
        "username": "jane_doe",
        "full_name": "Jane Doe",
        "is_active": True,
        "created_at": datetime.now()
    }
]

@router.get("/", response_model=List[User])
async def get_users():
    """
    Get all users
    """
    return fake_users_db

@router.get("/{user_id}", response_model=User)
async def get_user(user_id: int):
    """
    Get a specific user by ID
    """
    user = next((user for user in fake_users_db if user["id"] == user_id), None)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/", response_model=User)
async def create_user(user: UserCreate):
    """
    Create a new user
    """
    # Simulate user creation
    new_user = {
        "id": len(fake_users_db) + 1,
        **user.model_dump(exclude={"password"}),
        "is_active": True,
        "created_at": datetime.now()
    }
    fake_users_db.append(new_user)
    return new_user
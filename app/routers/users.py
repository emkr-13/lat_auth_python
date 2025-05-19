from fastapi import APIRouter, Depends, HTTPException, status
from models import User
from schemas import UserCreate, UserInDB
from tortoise.exceptions import DoesNotExist
from passlib.context import CryptContext
import uuid

router = APIRouter(tags=["users"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/users", response_model=UserInDB)
async def create_user(user: UserCreate):
    # Hash password
    hashed_password = pwd_context.hash(user.password)
    
    # Create user
    new_user = await User.create(
        email=user.email,
        username=user.username,
        fullname=user.fullname,
        password_hash=hashed_password
    )
    
    return new_user

@router.get("/users/{user_id}", response_model=UserInDB)
async def get_user(user_id: uuid.UUID):
    try:
        user = await User.get(id=user_id)
        return user
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="User not found")
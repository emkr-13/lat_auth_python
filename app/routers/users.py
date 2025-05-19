from fastapi import APIRouter, Depends, HTTPException, status
from app.models import User
from app.schemas import UserCreate, UserInDB, UserUpdate
from tortoise.exceptions import DoesNotExist
from passlib.context import CryptContext
from app.middleware.auth import get_current_active_user
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

@router.get("/users/me", response_model=UserInDB)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

@router.put("/users/me", response_model=UserInDB)
async def update_user_me(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_active_user)
):
    if user_update.password:
        current_user.password_hash = pwd_context.hash(user_update.password)
    if user_update.fullname:
        current_user.fullname = user_update.fullname
    if user_update.email:
        current_user.email = user_update.email
    if user_update.username:
        current_user.username = user_update.username
    
    await current_user.save()
    return current_user

@router.get("/users/{user_id}", response_model=UserInDB)
async def get_user(
    user_id: uuid.UUID,
    current_user: User = Depends(get_current_active_user)
):
    try:
        user = await User.get(id=user_id)
        return user
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="User not found")
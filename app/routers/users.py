from fastapi import APIRouter, Depends, HTTPException, status
from models import User
from schemas import UserCreate, UserInDB
from tortoise.exceptions import DoesNotExist

router = APIRouter(tags=["users"])

@router.post("/users", response_model=UserInDB)
async def create_user(user: UserCreate):
    # Hash password
    hashed_password = pwd_context.hash(user.password)
    
    # Create user
    new_user = await User.create(
        email=user.email,
        password=hashed_password,
        fullname=user.fullname
    )
    
    return new_user

@router.get("/users/{user_id}", response_model=UserInDB)
async def get_user(user_id: uuid.UUID):
    try:
        user = await User.get(id=user_id)
        return user
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="User not found")
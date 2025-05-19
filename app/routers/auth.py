from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
from app.models import User
from app.schemas import UserCreate, Token, UserInDB
from app.config import settings
from tortoise.exceptions import IntegrityError

router = APIRouter(tags=["auth"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)

@router.post("/register", response_model=UserInDB)
async def register(user_data: UserCreate):
    # Check if user already exists
    if await User.exists(email=user_data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    if await User.exists(username=user_data.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )
    
    # Create new user
    hashed_password = get_password_hash(user_data.password)
    try:
        user = await User.create(
            email=user_data.email,
            username=user_data.username,
            fullname=user_data.fullname,
            password_hash=hashed_password
        )
        return user
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error creating user"
        )

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await User.get_or_none(email=form_data.username)
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    
    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=timedelta(minutes=settings.access_token_expire_minutes)
    )
    
    refresh_token = create_access_token(
        data={"sub": user.email},
        expires_delta=timedelta(days=settings.refresh_token_expire_days)
    )
    
    user.refresh_token = refresh_token
    user.refresh_token_exp = datetime.utcnow() + timedelta(days=settings.refresh_token_expire_days)
    await user.save()
    
    return {"access_token": access_token, "token_type": "bearer", "refresh_token": refresh_token}

@router.post("/refresh-token")
async def refresh_token(refresh_token: str):
    try:
        payload = jwt.decode(refresh_token, settings.secret_key, algorithms=[settings.algorithm])
        email = payload.get("sub")
        user = await User.get_or_none(email=email)
        
        if not user or user.refresh_token != refresh_token:
            raise HTTPException(status_code=401, detail="Invalid refresh token")
            
        if user.refresh_token_exp < datetime.utcnow():
            raise HTTPException(status_code=401, detail="Refresh token expired")
            
        new_access_token = create_access_token(
            data={"sub": email},
            expires_delta=timedelta(minutes=settings.access_token_expire_minutes)
        )
        
        return {"access_token": new_access_token, "token_type": "bearer"}
        
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
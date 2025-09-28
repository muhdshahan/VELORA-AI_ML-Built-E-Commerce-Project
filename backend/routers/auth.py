from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from backend.schemas.user import UserCreate, UserLogin
from backend.schemas.token import Token
from backend.models.user import User
from backend.utils.security import hash_password, verify_password, create_access_token
from backend.db.database import get_db

router = APIRouter(prefix="/auth", tags=["auth"])

@router.get("/register")
async def landing():
    return {"message": "Welcome to registration"}

@router.post("/register")
async def register(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    q = await db.execute(select(User).filter((User.username == user_in.username) | (User.email == user_in.email)))
    existing = q.scalars().first()
    if existing:
        raise HTTPException(status_code=400, detail="Username or email already exists")
    
    user = User(
        username=user_in.username,
        email=user_in.email,
        hashed_password=hash_password(user_in.password),
        role=user_in.role
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

@router.get("/login")
async def landing():
    return {"message": "Welcome to login"}

@router.post("/login", response_model=Token)
async def login(form_data: UserLogin, db: AsyncSession = Depends(get_db)):
    q = await db.execute(select(User).filter(User.email == form_data.email))
    user = q.scalars().first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token({"sub": user.username})
    return {"user_id": user.id, "access_token": access_token, "token_type": "bearer", "role": user.role }

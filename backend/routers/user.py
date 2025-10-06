from fastapi import APIRouter, Depends
from backend.schemas.user import UserOut
from backend.utils.dependencies import get_current_user

router = APIRouter()

@router.get("/users/me")
async def get_me(current_user = Depends(get_current_user)):
    return current_user

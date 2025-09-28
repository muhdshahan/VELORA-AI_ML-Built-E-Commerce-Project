from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from backend.db.database import get_db
from backend.models import Feedback
from backend.schemas.feedback import FeedbackCreate

router = APIRouter(prefix="/feedback", tags=["Feedback"])

@router.post("/")
async def create_feedback(feedback: FeedbackCreate, db: AsyncSession = Depends(get_db)):
    new_feedack = Feedback(user_id=feedback.user_id, text=feedback.text)
    db.add(new_feedack)
    await db.commit()
    await db.refresh(new_feedack)
    return new_feedack

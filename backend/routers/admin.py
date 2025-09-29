import logging
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from backend.db.database import get_db  
from backend.models import User, Feedback  
from backend.schemas.user import UserOut
from backend.ml.sentiment import analyze_sentiment

# Basic logger setup
logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s [%(levelname)s]: %(message)s"
)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/admin", tags=["Admin"])

async def get_user_sentiment(db: AsyncSession, user_id: int):
    result = await db.execute(select(Feedback).where(Feedback.user_id == user_id))
    feedbacks = result.scalars().all()
    # Run sentiment analysis
    if not feedbacks:
        return "No Feedback yet"
    # Concatenate all feedback texts, run a sentiment analyser
    feedback_texts = " ". join([f.text for f in feedbacks])
    logger.info(f"Retrieved feedbacks:{feedback_texts}")
    sentiment = analyze_sentiment(feedback_texts)
    logger.info(f"Sentiment:{sentiment}")
    logger.info(f"Sentiment:{type(sentiment)}")
    return sentiment

@router.get("/allusers", response_model=list[UserOut])
async def get_users(db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(User))
        users = result.scalars().all()
        output = []

        logger.info(f"Fetched {len(users)} users.")
        for user in users:
            if user.role != "admin":
                logger.info(f"Current user:{user.id}")
                sentiment = await get_user_sentiment(db, user.id)
                output.append(UserOut(
                    id=user.id,
                    username=user.username,
                    email=user.email,
                    sentiment=sentiment
                ))
        logger.info(f"output is: {output}")
        return output
    
    except Exception as e:
        logger.error(f"Error in get_users: {e}")
        return []
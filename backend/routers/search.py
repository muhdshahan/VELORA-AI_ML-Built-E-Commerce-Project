from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from backend.db.database import get_db
from backend.ml.smart_search import semantic_search
from backend.schemas.search import SearchRequest

router = APIRouter(prefix="/search", tags=["search"])

@router.post("/smart")
async def run_semantic_search(request: SearchRequest, db: AsyncSession = Depends(get_db)):
    if not request.query:
        raise HTTPException(status_code=400, detail="No query provided.")
    results = await semantic_search(request.query, db)
    return results

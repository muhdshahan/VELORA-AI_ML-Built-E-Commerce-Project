from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from backend.db.database import get_db
from backend.ml.smart_search import semantic_search
from backend.schemas.product import ProductOut

router = APIRouter(prefix="/search", tags=["search"])

@router.post("/smart", response_model=list[ProductOut])
async def run_semantic_search(query: str, db: AsyncSession = Depends(get_db)):
    # term = query.get("query")
    if not query:
        raise HTTPException(status_code=400, detail="No query provided.")
    results = await semantic_search(query, db)
    return results

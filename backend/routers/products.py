from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from backend.db.database import get_db
from backend.models.product import Product
from backend.schemas.product import ProductCreate, ProductOut
from backend.utils.dependencies import get_current_user, get_current_admin
from backend.ml.recommender import collaborative_recommendations
from backend.models.activity import Activity

router = APIRouter(prefix="/products", tags=["products"])

# Admin creates product
@router.post("/", response_model=ProductOut, dependencies=[Depends(get_current_admin)])
async def create_product(product_in: ProductCreate, db: AsyncSession = Depends(get_db)):
    product = Product(**product_in.dict())
    db.add(product)
    await db.commit()
    await db.refresh(product)
    return product

# List products (public)
@router.get("/", response_model=list[ProductOut])
async def list_products(db: AsyncSession = Depends(get_db)):
    q = await db.execute(select(Product))
    return q.scalars().all()

# Get single product view: logs 'viewed', returns collaborative recommendations
@router.get("/view{product_id}")
async def view_product(product_id: int, db:AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    # fetch product
    q = await db.execute(select(Product).filter(Product.id==product_id))
    product = q.scalars().first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # log activity (view)
    activity = Activity(
        user_id=current_user.id,
        product_id=product.id,
        action="viewed",
        time_spent=0.0
        )
    db.add(activity)
    await db.commit()

    # get collaborative recommendations
    recommendations = await collaborative_recommendations(db, product.id, limit=6)
    return recommendations


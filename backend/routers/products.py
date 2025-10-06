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
@router.post("/", response_model=ProductOut)
async def create_product(product_in: ProductCreate, db: AsyncSession = Depends(get_db)):
    product = Product(
        name=product_in.name,
        category=product_in.category,
        description=product_in.description,
        price=product_in.price,
        stock=product_in.stock,
        image_url=product_in.image_url
    )
    db.add(product)
    await db.commit()
    await db.refresh(product)
    return product

# List products (public)
@router.get("/", response_model=list[ProductOut])
async def list_products(db: AsyncSession = Depends(get_db)):
    q = await db.execute(select(Product))
    return q.scalars().all()

# Single product endpoint
@router.get("/{product_id}", response_model=ProductOut)
async def get_product(product_id: int, db: AsyncSession = Depends(get_db)):
    q = await db.execute(select(Product).filter(Product.id == product_id))
    product = q.scalars().first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.get("/recommended/{product_id}", response_model=list[ProductOut])
async def get_recommended_products(product_id: int, db: AsyncSession = Depends(get_db)):
    recommendations = await collaborative_recommendations(db, product_id)
    return recommendations

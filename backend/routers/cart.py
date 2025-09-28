from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from backend.db.database import get_db
from backend.schemas.cart import CartAdd, CartItemOut
from backend.models.cart import CartItem
from backend.models.activity import Activity
from backend.models.product import Product
from backend.utils.dependencies import get_current_user

router = APIRouter(prefix="/cart", tags=["cart"])

@router.post("/add", response_model=CartItemOut)
async def add_to_cart(item: CartAdd, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    # check product exists
    q = await db.execute(select(Product).filter(Product.id == item.product_id))
    product = q.scalars().first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # create cart item
    q2 = await db.execute(select(CartItem).filter(CartItem.user_id == current_user.id, CartItem.product_id == item.product_id))
    cart_item = CartItem(
        user_id=current_user.id,
        product_id=item.product_id,
        quantity=item.quantity
    )
    db.add(cart_item)
    await db.commit()
    await db.refresh(cart_item)

    # log activity
    act = Activity(
        user_id=current_user.id,
        product_id=product.id,
        action="added_to_cart",
        time_spent=0.0
        )
    db.add(act)
    await db.commit()

    return cart_item

# View cart
@router.get("/", response_model=list[CartItemOut])
async def view_cart(db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    q = await db.execute(select(CartItem).filter(CartItem.user_id == current_user.id))
    return q.scalars().all()

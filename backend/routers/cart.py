from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from backend.db.database import get_db
from backend.schemas.cart import CartAdd, CartItemOut
from backend.models.cart import CartItem
from backend.models.activity import Activity
from backend.models.product import Product
from backend.utils.dependencies import get_current_user
from sqlalchemy.orm import selectinload

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
    existing_cart_item = q2.scalars().first()
    if existing_cart_item:
        # Optionally update quantity
        existing_cart_item.quantity += item.quantity
        await db.commit()
        await db.refresh(existing_cart_item)
        cart_item = existing_cart_item
    else:
        # Create new cart item
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

    # Reload cart item with product for response
    q3 = await db.execute(
        select(CartItem)
        .options(selectinload(CartItem.product))
        .filter(CartItem.id == cart_item.id)
    )
    cart_item_with_product = q3.scalars().first()

    return cart_item_with_product

# View cart
@router.get("/", response_model=list[CartItemOut])
async def view_cart(db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    q = await db.execute(select(CartItem).options(selectinload(CartItem.product)).filter(CartItem.user_id == current_user.id))
    return q.scalars().unique().all()

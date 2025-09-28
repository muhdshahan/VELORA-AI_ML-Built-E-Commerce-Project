from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from backend.db.database import get_db
from backend.models.cart import CartItem
from backend.models.order import Order
from backend.models.product import Product
from backend.models.activity import Activity
from backend.utils.dependencies import get_current_user

router = APIRouter(prefix="/orders", tags=["orders"])

@router.post("/checkout")
async def checkout(db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    # get user's cart
    q = await db.execute(select(CartItem).filter(CartItem.user_id == current_user.id))
    cart_items = q.scalars().all()
    if not cart_items :
        raise HTTPException(status_code=400, detail="Cart is empty")
    
    created_orders = []
    for item in cart_items:
        # fetch product to compute price and verify stock
        qprod = await db.execute(select(Product).filter(Product.id == item.product_id))
        product = qprod.scalars().first()

        # create order record
        order = Order(user_id=current_user.id, product_id=product.id, quantity=item.quantity, total_price=product.price)
        db.add(order)

        # log activity as purchase
        act = Activity(user_id=current_user.id, product_id=product.id, action="purchased", time_spent=0.0)
        db.add(act)

        created_orders.append(order)

    # delete cart items
    for item in cart_items:
        await db.delete(item)

    await db.commit()

    return {"msg": "checkout successful", "orders_created": len(created_orders)}

# View Orders
@router.get("/", response_model=list)
async def list_orders(db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    q = await db.execute(select(Order).filter(Order.user_id == current_user.id))
    return q.scalars().all()
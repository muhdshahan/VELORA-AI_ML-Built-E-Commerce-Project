from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from backend.db.database import get_db
from backend.models.cart import CartItem
from backend.models.order import Order
from backend.models.product import Product
from backend.models.activity import Activity
from backend.utils.dependencies import get_current_user
from backend.ml.sales_forecast import get_daily_sales, forecast_sales


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

# Daily sales for a single user
@router.get("/user/{user_id}/sales")
async def user_sales(user_id: int, db: AsyncSession = Depends(get_db)):
    q = await db.execute(
        select(func.date(Order.created_at).label("day"),
               func.sum(Order.total_price).label("total_sales"))
        .filter(Order.user_id == user_id)
        .group_by(func.date(Order.created_at))
        .order_by("day")
    )
    sales = q.all()

    total_sales = sum(row.total_sales for row in sales) if sales else 0

    return {
        "daily_sales": [{"day": str(row.day), "total_sales": row.total_sales} for row in sales],
        "total_sales": total_sales
    }

# Overall daily sales across all users
@router.get("/sales/overall")
async def overall_sales(db: AsyncSession = Depends(get_db)):
    q = await db.execute(
        select(func.date(Order.created_at).label("day"),
               func.sum(Order.total_price).label("total_sales"))
        .group_by(func.date(Order.created_at))
        .order_by("day")
    )
    sales = q.all()
    return [{"day": str(row.day), "total_sales": row.total_sales} for row in sales]


# Get daily sales (overall or by user)
@router.get("/sales/daily")
async def daily_sales(
    user_id: int = Query(None, description="Optional: filter sales for a specific user"),
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Returns daily sales aggregated by date.
    Optional: Filter by user_id.
    """
    df = await get_daily_sales(db, user_id=user_id)
    return df.to_dict(orient="records")


# Forecast sales (overall or by user)
@router.get("/sales/forecast")
async def sales_forecast_endpoint(
    periods: int = Query(30, description="Number of days to forecast"),
    user_id: int = Query(None, description="Optional: forecast for specific user"),
    db: AsyncSession = Depends(get_db)
):
    """
    Forecast sales for either all users or a specific user.
    """
    forecast = await forecast_sales(db, periods=periods, user_id=user_id)
    return forecast
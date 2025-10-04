import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select
from backend.models.user import User
from backend.models.order import Order
from datetime import datetime

async def segement_customers(db: AsyncSession, n_clusters=3):
    """
    ML-based customer segmentation using KMeans.
    """

    # Step 1: Fetch user sales data
    result = await db.execute(select(
        Order.user_id,
        func.count(Order.id).label("num_orders"),
        func.sum(Order.total_price).label("total_spent"),
        func.max(Order.created_at).label("last_order")
        ).group_by(Order.user_id))
    
    user_stats = result.all()
    
    if not user_stats:
        return {"msg": "No sales data for segmentation"}
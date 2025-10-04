import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select
from backend.models.user import User
from backend.models.order import Order
from datetime import datetime

async def segment_customers(db: AsyncSession, n_clusters=3):
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
    
    df = pd.DataFrame(user_stats, columns=["user_id", "num_orders", "total_spent", "last_order"])
    df["recency_days"] = (datetime.now() - df["last_order"]).dt.days

    # Step 2: Prepare features
    features = df[["num_orders", "total_spent", "recency_days"]]
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(features)

    # Step 3: KMeans clustering
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    df["cluster"] = kmeans.fit_predict(X_scaled)

    # Step 4: Map cluster numbers to tiers
    # Example: cluster with highest total_spend = Platinum
    cluster_means = df.groupby("cluster")["total_spent"].mean().sort_values(ascending=False)
    tier_map = {cluster: tier for cluster, tier in zip(cluster_means.index, ["Platinum", "Gold", "Silver"])}
    df["tier"] = df["cluster"].map(tier_map)

    # Step 5: Update users in DB
    for _, row in df.iterrows():
        await db.execute(
            User.__table__.update()
            .where(User.id == row["user_id"]
            .values(tier=row["tier"]))
        )
    await db.commit()

    return {"msg": "Customer segmentation done via KMeans", "details": df[["user_id", "tier"]].to_dict(orient="records")}
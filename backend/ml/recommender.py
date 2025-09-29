import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sklearn.metrics.pairwise import cosine_similarity
from backend.models.activity import Activity
from backend.models.product import Product
from typing import List

async def collaborative_recommendations(db: AsyncSession, user_id: int, top_n: int = 4):
    """
    Collaborative Filtering using user-product interaction matrix.
    """

    # Load interactions
    q = await db.execute(select(Activity.user_id, Activity.product_id, Activity.action))
    data = q.all()
    if not data:
        return []
    
    df = pd.DataFrame(data, columns=["user_id", "product_id", "action"])

    action_score_map = {
    "viewed": 1,
    "added_to_cart": 2,
    "purchased": 3
    }
    df["score"] = df["action"].map(action_score_map).fillna(0)

    # Build product matrix
    user_product_matrix = (
        df.pivot_table(index="user_id", columns="product_id", values="score", aggfunc="sum", fill_value=0)
    )

    if user_id not in user_product_matrix:
        return []
    
    # Compute cosine similarity between users
    similarity = cosine_similarity(user_product_matrix)
    sim_df = pd.DataFrame(similarity, index=user_product_matrix.index, columns=user_product_matrix.index)

    if user_id not in sim_df.columns:
        return []
    # Find top similar users
    similar_users = sim_df[user_id].sort_values(ascending=False).drop(user_id).head(top_n).index

    # Get products purchased by similar users
    similar_users_data = user_product_matrix.loc[similar_users]
    scores = similar_users_data.sum(axis=0)

    # Exclude products the user already interacted with
    user_products = set(user_product_matrix.loc[user_id][user_product_matrix.loc[user_id]>0].index)
    scores = scores.drop(labels=user_products, errors="ignore")

    if scores.empty:
        return []
    
    # Get top-N product IDs
    recommended_ids = scores.sort_values(ascending=False).head(top_n).index.to_list()

    q2 = await db.execute(select(Product).filter(Product.id.in_(recommended_ids)))
    products = q2.scalars().all()

    # keep order
    prod_map = {p.id: p for p in products}
    return [prod_map[pid] for pid in recommended_ids if pid in prod_map]
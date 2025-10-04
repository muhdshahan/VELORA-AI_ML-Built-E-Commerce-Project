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
import pandas as pd
from prophet import Prophet
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from backend.models.order import Order

async def get_daily_sales(db: AsyncSession):
    """
    Fetches aggregated daily sales from the DB
    Returns: DataFrame with columns ['ds', 'y']
    """
    q = await db.execute(
        select(
            func.date(Order.created_at).label("ds"),
            func.sum(Order.total_price).label("y")
        )
        .group_by(func.date(Order.created_at))
        .order_by("ds")
    )
    results = q.all()

    if not results:
        return pd.DataFrame(columns=["ds", "y"])

    df = pd.DataFrame(results, columns=["ds", "y"])
    return df


async def forecast_sales(db: AsyncSession, periods: int = 30):
    """
    Train Prophet model and forecast future sales
    periods: number of days to forecast
    """
    df = await get_daily_sales(db)

    if df.empty:
        return {"msg": "No sales data available"}

    model = Prophet(daily_seasonality=True, yearly_seasonality=True)
    model.fit(df)

    future = model.make_future_dataframe(periods=periods)
    forecast = model.predict(future)

    # Return essential columns
    forecast_out = forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]].tail(periods)
    return forecast_out.to_dict(orient="records")

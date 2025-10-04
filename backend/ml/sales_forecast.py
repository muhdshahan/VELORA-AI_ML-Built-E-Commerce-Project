import pandas as pd
from prophet import Prophet
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from backend.models.order import Order


# Fetch daily sales (overall or by user)
async def get_daily_sales(db: AsyncSession, user_id: int = None):
    """
    Fetch aggregated daily sales from the DB.
    If user_id is provided, fetch sales only for that user.
    Returns: DataFrame with columns ['ds', 'y']
    """
    query = select(
        func.date(Order.created_at).label("ds"),
        func.sum(Order.total_price).label("y")
    )

    if user_id:
        query = query.where(Order.user_id == user_id)

    query = query.group_by(func.date(Order.created_at)).order_by("ds")
    result = await db.execute(query)
    rows = result.all()

    if not rows:
        return pd.DataFrame(columns=["ds", "y"])

    df = pd.DataFrame(rows, columns=["ds", "y"])
    return df

# Forecast sales
async def forecast_sales(db: AsyncSession, periods: int = 30, user_id: int = None):
    """
    Forecast future sales using Prophet.
    periods: number of days to forecast
    user_id: optional, forecast for specific user
    """
    df = await get_daily_sales(db, user_id=user_id)

    if df.empty:
        return {"msg": "No sales data available"}

    model = Prophet(daily_seasonality=True, yearly_seasonality=True)
    model.fit(df)

    future = model.make_future_dataframe(periods=periods)
    forecast = model.predict(future)

    # Return essential columns
    forecast_out = forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]].tail(periods)
    forecast_out['yhat'] = forecast_out['yhat'].clip(lower=0)
    forecast_out['yhat_lower'] = forecast_out['yhat_lower'].clip(lower=0)
    forecast_out['yhat_upper'] = forecast_out['yhat_upper'].clip(lower=0)
    forecast_out['ds'] = forecast_out['ds'].dt.date


    return forecast_out.to_dict(orient="records")

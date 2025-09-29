""" Entry point """

from fastapi import FastAPI
from backend.routers import auth, products, orders, admin, feedback, search, cart
from backend.db.database import engine, Base

app = FastAPI(title="Velora - Premium Jewels & Clothing")

# Register routers
app.include_router(auth.router)
app.include_router(products.router)
app.include_router(orders.router)
app.include_router(admin.router)
app.include_router(feedback.router)
app.include_router(cart.router)
# app.include_router(search.router)

@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        # create all tables from imported models
        await conn.run_sync(Base.metadata.create_all)

@app.get("/")
async def root():
    return {"message": "Welcome to Velora API"}


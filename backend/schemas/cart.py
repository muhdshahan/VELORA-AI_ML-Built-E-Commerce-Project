from pydantic import BaseModel

class CartAdd(BaseModel):
    product_id: int
    quantity: int = 1

class CartItemOut(BaseModel):
    id: int

    class Config:
        orm_mode = True
from typing import Optional
from pydantic import BaseModel
from backend.schemas.product import ProductOut

class CartAdd(BaseModel):
    product_id: int
    quantity: int 
    price: Optional[float]

class CartItemOut(BaseModel):
    id: int
    product_id: int
    quantity: int
    product: Optional[ProductOut]  # mark as optional to be safe

    class Config:
        orm_mode = True

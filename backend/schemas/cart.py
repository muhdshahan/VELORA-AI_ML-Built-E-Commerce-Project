from pydantic import BaseModel
from backend.schemas.product import ProductOut

class CartAdd(BaseModel):
    product_id: int
    quantity: int 

class CartItemOut(BaseModel):
    id: int
    product_id: int
    quantity: int
    product: ProductOut  
    class Config:
        orm_mode = True
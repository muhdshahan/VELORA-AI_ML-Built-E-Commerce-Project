from pydantic import BaseModel

class ProductBase(BaseModel):
    name: str
    category: str
    description: str
    price: float
    stock: int
    image_url: str

class ProductCreate(ProductBase):
    pass 

class ProductOut(ProductBase):
    id: int

    class Config:
        orm_mode = True
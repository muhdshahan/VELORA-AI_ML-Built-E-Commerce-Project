from pydantic import BaseModel

class OrderCreate(BaseModel):
    # for simple checkout, we can allow purchase of entire cart via endpoint with no payload
    pass 

class OrderOut(BaseModel):
    id: int

    class Config:
        orm_model = True
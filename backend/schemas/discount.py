from pydantic import BaseModel

class TierDiscountUpdate(BaseModel):
    tier: str
    discount: int = Field(..., ge=1, le=90)

    class Config:
        orm_mode=True
    
from pydantic import BaseModel, Field

class TierDiscountUpdate(BaseModel):
    tier: str
    discount_percentage: int = Field(..., ge=1, le=90)

    class Config:
        orm_mode=True
    
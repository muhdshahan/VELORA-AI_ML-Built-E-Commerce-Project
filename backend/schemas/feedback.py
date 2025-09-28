from pydantic import BaseModel

class FeedbackCreate(BaseModel):
    user_id: int
    text: str

    class Config:
        orm_mode=True
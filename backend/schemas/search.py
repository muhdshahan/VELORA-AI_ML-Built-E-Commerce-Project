from pydantic import BaseModel

class SearchRequest(BaseModel):
    query: str

    class Config:
        orm_mode=True
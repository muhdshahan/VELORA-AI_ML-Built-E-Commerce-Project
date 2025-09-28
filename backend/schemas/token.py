from pydantic import BaseModel

class Token(BaseModel):
    user_id: int
    access_token: str
    token_type: str
    role: str
from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    id: int
    email: str
    full_name: Optional[str] = None
    hashed_password: str

    class Config:
        orm_mode = True
        from_attributes = True

class UserIn(BaseModel):
    email: str
    full_name: Optional[str] = None
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

from pydantic import BaseModel
from typing import Optional, List


class User(BaseModel):
    email: str
    full_name: Optional[str] = None
    hashed_password: str


class UserIn(BaseModel):
    email: str
    full_name: Optional[str] = None
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class Document(BaseModel):
    id: int
    title: str
    content: str = ""
    owner: str
    last_modified: str = ""
    # shared_with: List[str] = []
    # public_token: Optional[str] = None

from pydantic import BaseModel


class User(BaseModel):
    email: str
    full_name: str | None = None
    hashed_password: str


class UserIn(BaseModel):
    email: str
    full_name: str | None = None
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

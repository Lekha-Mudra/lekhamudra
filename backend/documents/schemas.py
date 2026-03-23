from pydantic import BaseModel
from typing import Optional, List

class Document(BaseModel):
    id: int
    title: str
    content: str = ""
    owner: str
    last_modified: str = ""
    # shared_with: List[str] = []
    # public_token: Optional[str] = None

    class Config:
        orm_mode = True
        from_attributes = True

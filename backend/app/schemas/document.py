import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class DocumentBase(BaseModel):
    title: str
    content: str = ""


class DocumentCreate(DocumentBase):
    pass


class DocumentUpdate(BaseModel):
    title: str | None = None
    content: str | None = None


class DocumentInDBBase(DocumentBase):
    id: uuid.UUID
    owner_id: uuid.UUID
    last_modified: datetime
    version: int
    model_config = ConfigDict(from_attributes=True)


class Document(DocumentInDBBase): ...  # response model


class DocumentInDB(DocumentInDBBase): ...  # internal use

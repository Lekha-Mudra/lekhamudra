import uuid

from pydantic import BaseModel, ConfigDict, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    full_name: str | None = None


class UserCreate(UserBase):
    password: str


class UserInDBBase(UserBase):
    id: uuid.UUID
    model_config = ConfigDict(from_attributes=True)


class User(UserInDBBase): ...  # exported to clients


class UserInDB(UserInDBBase):
    hashed_password: str  # internal use

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class AccountBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=20)
    admin: bool = False
    active: bool = True
    created_at: Optional[int] = None

class AccountCreate(AccountBase):
    password: str

class AccountResponse(AccountBase):
    id: int

    class Config:
        from_attributes = True

from typing import Annotated
from annotated_types import MinLen, MaxLen
from pydantic import BaseModel, ConfigDict


class AccountCreate(BaseModel):
    # username: str = Field(..., min_length=3, max_length=20)
    username: Annotated[str, MinLen(3), MaxLen(20)]
    password: bytes
    admin: bool = False
    active: bool = True
    created_at: int


class UserSchema(BaseModel):
    model_config = ConfigDict(strict=True)

    username: str
    password: bytes
    #email: EmailStr | None = None
    admin: bool = False
    active: bool = True
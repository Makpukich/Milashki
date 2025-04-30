from pydantic import EmailStr
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import registry

from users.schemas import UserSchema
from .base import Base

class Account(Base):
    __tablename__ = "accounts"
    username: Mapped[str]
    password: Mapped[bytes]
    admin: Mapped[bool]
    active: Mapped[bool]
    description: Mapped[str]
    created_at: Mapped[int]
'''username: str
    password: bytes
    email: EmailStr | None = None
    admin: bool = False
    active: bool = True'''
from sqlalchemy.orm import Mapped
from .base import Base

class Account(Base):
    __tablename__ = "accounts"
    id: Mapped[int]
    username: Mapped[str]
    password: Mapped[bytes]
    admin: Mapped[bool]
    active: Mapped[bool]
    created_at: Mapped[int]
'''username: str
    password: bytes
    email: EmailStr | None = None
    admin: bool = False
    active: bool = True'''

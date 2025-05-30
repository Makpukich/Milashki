from sqlalchemy import Column, Integer, String, Boolean
from .base import Base

class Account(Base):
    __tablename__ = "accounts"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    username = Column(String(20), unique=True, nullable=False)
    password = Column(String(128), nullable=False)
    admin = Column(Boolean, default=False)
    active = Column(Boolean, default=True)
    created_at = Column(Integer)


"""class Account(Base):
    __tablename__ = "accounts"
    id: Mapped[int]
    username: Mapped[str]
    password: Mapped[bytes]
    admin: Mapped[bool]
    active: Mapped[bool]
    created_at: Mapped[int]"""
'''username: str
    password: bytes
    email: EmailStr | None = None
    admin: bool = False
    active: bool = True'''

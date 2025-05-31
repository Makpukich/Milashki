from sqlalchemy import Column, Integer, String, Boolean
from .base import Base


class Wallet(Base):
    __tablename__ = "wallets"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    user_id = Column(Integer)
    balance = Column(Integer)

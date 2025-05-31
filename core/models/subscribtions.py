from sqlalchemy import Column, Integer, String
from .base import Base

class Subscription(Base):
    __tablename__ = "subscriptions"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    cost = Column(Integer)
    duration = Column(Integer)
    access = Column(String)
    name = Column(String)


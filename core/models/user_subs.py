from sqlalchemy import Column, Integer, String
from .base import Base

class UserSubscription(Base):
    __tablename__ = "userSubs"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    user_id = Column(Integer)
    subscription_id = Column(Integer)
    purchased_in = Column(Integer)


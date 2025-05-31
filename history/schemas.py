from pydantic import BaseModel
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class SubscriptionPurchase(BaseModel):
    __tablename__ = "subscription_purchases"
    wallet_id: int
    subscription_type_id: int
    purchase_date: int


class SubscriptionResponse(SubscriptionPurchase):
    id: int

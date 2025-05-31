from pydantic import BaseModel, Field, ConfigDict

class SubscriptionBase(BaseModel):
    name: str
    access: str
    duration: int
    cost: int

class SubscriptionResponse(SubscriptionBase):
    id: int
    class Config:
        from_attributes = True
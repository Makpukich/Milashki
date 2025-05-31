from pydantic import BaseModel, Field, ConfigDict

class UserSubsBase(BaseModel):
    user_id: int
    subscription_id: int
    purchased_in: int

class UserSubsResponse(UserSubsBase):
    id: int
    class Config:
        from_attributes = True
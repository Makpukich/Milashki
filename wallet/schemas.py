from pydantic import BaseModel


class WalletBase(BaseModel):
    balance: int
    user_id: int


class WalletResponse(WalletBase):
        id: int

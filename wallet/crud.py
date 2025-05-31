from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Wallet as WalletModel
from wallet.schemas import WalletResponse


async def get_wallet_by_wallet_id(session: AsyncSession, wallet_id: int) -> WalletModel | None:
    result = await session.get(WalletModel, wallet_id)
    return result


async def get_wallet_by_user_id(session: AsyncSession, user_id: int) -> WalletModel | None:
    stmt = select(WalletModel).where(user_id == WalletModel.user_id)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def change_wallet_balance(session: AsyncSession, top_up: bool, user_id: int, money: int) -> WalletResponse | None:
    wallet = await get_wallet_by_user_id(session, user_id)
    if wallet == None:
        raise HTTPException(status_code=404, detail="Wallet not found")
    if top_up:
        wallet.balance += money
    elif wallet.balance < money:
        raise HTTPException(status_code=402, detail="Account not found")
    else:
        wallet.balance -= money
#       success!
    await session.commit()
    await session.refresh(wallet)
    return wallet

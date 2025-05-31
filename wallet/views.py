from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from wallet.schemas import WalletResponse
from wallet.crud import get_wallet_by_wallet_id, get_wallet_by_user_id, change_wallet_balance
from core.models import db_helper, Account

router = APIRouter(tags=["Wallets"])


@router.get("/wallets/{user_id}", response_model=WalletResponse)
async def read_wallet_by_user_id(
    user_id: int,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    wallet = await get_wallet_by_user_id(session, user_id)
    if wallet is None:
        raise HTTPException(status_code=404, detail="Wallet not found")
    return wallet


@router.get("/wallets/{wallet_id}", response_model=WalletResponse)
async def read_wallet_by_wallet_id(
    wallet_id: int,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    wallet = await get_wallet_by_wallet_id(session, wallet_id)
    if wallet is None:
        raise HTTPException(status_code=404, detail="Wallet not found")
    return wallet


@router.put("/wallets/{wallet_id}", response_model=WalletResponse)
async def top_up_balance(
    user_id: int,
    top_up: bool,
    money: int,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    wallet = await change_wallet_balance(session, top_up=top_up, user_id=user_id, money=money)
    if wallet is None:
        raise HTTPException(status_code=404, detail="Wallet not found")
    return wallet

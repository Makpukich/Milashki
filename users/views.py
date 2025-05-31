from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from auth.utils import hash_password

from users.schemas import AccountResponse, AccountCreate
from users.crud import get_accounts, get_account_by_id, create_account, update_account, delete_account, \
    get_account_by_name
from core.models import db_helper, Account
from api.auth.views import get_current_account

router = APIRouter(tags=["Accounts"])


@router.post("/accounts/", response_model=AccountResponse)
async def create_new_account(
        account_in: AccountCreate,
        session: AsyncSession = Depends(db_helper.session_dependency),
):
    existing = await get_account_by_name(session, account_in.username)
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")

    account_in.password = hash_password(account_in.password)

    return await create_account(session, account_in)


@router.get("/accounts/", response_model=list[AccountResponse])
async def read_accounts(
        session: AsyncSession = Depends(db_helper.session_dependency),
        current_user: Account = Depends(get_current_account),
):
    if not current_user.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin can view all accounts"
        )
    return await get_accounts(session)


@router.get("/accounts/{account_id}", response_model=AccountResponse)
async def read_account(
        account_id: int,
        session: AsyncSession = Depends(db_helper.session_dependency),
        current_user: Account = Depends(get_current_account),
):
    if not current_user.admin and current_user.id != account_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only view your own account"
        )

    account = await get_account_by_id(session, account_id)
    if account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return account


@router.put("/accounts/{account_id}", response_model=AccountResponse)
async def update_existing_account(
        account_id: int,
        account_in: AccountCreate,
        session: AsyncSession = Depends(db_helper.session_dependency),
        current_user: Account = Depends(get_current_account),
):
    if not current_user.admin and current_user.id != account_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update your own account"
        )

    account = await update_account(session, account_id, account_in)
    if account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return account


@router.delete("/accounts/{account_id}", response_model=AccountResponse)
async def delete_existing_account(
        account_id: int,
        session: AsyncSession = Depends(db_helper.session_dependency),
        current_user: Account = Depends(get_current_account),
):
    if not current_user.admin and current_user.id != account_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your own account"
        )

    account = await delete_account(session, account_id)
    if account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return account
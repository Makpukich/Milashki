from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from  sqlalchemy.engine import Result

from auth.utils import hash_password
from datetime import datetime

from core.models import Account as AccountModel
from users.schemas import AccountCreate, AccountResponse
from core.models import Account


async def get_accounts(session: AsyncSession) -> list[AccountModel]:
    stmt = select(AccountModel).order_by(AccountModel.id)
    result = await session.execute(stmt)
    return result.scalars().all()

async def get_account_by_id(session: AsyncSession, account_id: int) -> AccountModel | None:
    account = await session.get(AccountModel, account_id)
    return account

async def get_account_by_name(session: AsyncSession, account_name: str) -> AccountModel | None:
    account = await session.get(AccountModel, account_name)
    return account


async def create_account(
        session: AsyncSession,
        account_in: AccountCreate
) -> Account:
    existing_account = await session.execute(
        select(Account).where(Account.username == account_in.username)
    )
    if existing_account.scalar_one_or_none() is not None:
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )
    hashed_password = hash_password(account_in.password)

    account = Account(
        username=account_in.username,
        password=hashed_password,
        admin=account_in.admin,
        active=account_in.active,
        created_at=int(datetime.now().timestamp())
    )

    session.add(account)
    await session.commit()
    await session.refresh(account)

    return account

async def update_account(session: AsyncSession, account_id: int, new_account: AccountResponse) -> AccountResponse | None:
    account = await get_account_by_id(session, account_id)
    if account:
        account.username = new_account.username
        account.password = new_account.password
        account.admin = new_account.admin
        account.active = new_account.active
    await session.commit()
    await session.refresh(account)
    return account

async def delete_account(session: AsyncSession, account_id) -> AccountResponse | None:
    account = await get_account_by_id(session, account_id)

    if account is None:
        raise HTTPException(
            status_code=404,
            detail="Account not found"
        )

    await session.delete(account)
    await session.commit()
    return account




"""from users.schemas import CreateUser


def create_user(user_in: CreateUser) -> dict:
    user = user_in.model_dump()
    return {
        "success": True,
        "user": user,
    }
"""
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from  sqlalchemy.engine import Result

from users.schemas import AccountCreate
from core.models import Account
async  def get_accounts(session: AsyncSession) -> list[Account]:
    stmt = select(Account).order_by(Account.id)
    result: Result = await session.execute(stmt)
    accounts = result.scalars().all()
    return list(accounts)

async def get_account(session: AsyncSession, account_id: int) -> Account | None:
    return await session.get(Account, account_id)

async def create_account(session: AsyncSession, account_in: AccountCreate) -> Account:
    account = Account(**account_in.model_dump())
    session.add(account)
    await session.commit()
    await session.refresh(account)
    return account

async def update_account(session: AsyncSession, account_id: int, new_account: Account) -> Account | None:
    account = get_account(session, account_id)
    if account:
        account.username = new_account.username
        account.password = new_account.password
        account.admin = new_account.admin
        account.active = new_account.active
    await session.commit()
    await session.refresh(account)
    return account

async def delete_account(session: AsyncSession, account_id) -> Account | None:
    account = get_account(session, account_id)
    if account:
        await session.delete(account)
    await session.commit()
    await session.refresh(account)
    return account




"""from users.schemas import CreateUser


def create_user(user_in: CreateUser) -> dict:
    user = user_in.model_dump()
    return {
        "success": True,
        "user": user,
    }
"""
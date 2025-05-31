from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from datetime import datetime

from core.models import Subscription as SubscriptionModel
from users.schemas import SubscriptionCreate, SubscriptionResponse


async def get_subscriptions(session: AsyncSession) -> list[SubscriptionModel]:
    stmt = select(SubscriptionModel).order_by(SubscriptionModel.id)
    result = await session.execute(stmt)
    return result.scalars().all()

async def get_subscription(session: AsyncSession, account_id: int) -> SubscriptionModel | None:
    account = await session.get(SubscriptionModel, account_id)
    return account

async def create_subscription(
        session: AsyncSession,
        subscription_in: SubscriptionCreate
) -> SubscriptionModel:
    existing_account = await session.execute(
        select(SubscriptionModel).where(subscription_in.name == Subscription.name)
    )
    if existing_account.scalar_one_or_none() is not None:
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )

    account = Account(
        username=account_in.username,
        password=account_in.password,
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



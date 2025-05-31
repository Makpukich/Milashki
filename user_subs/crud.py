from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from datetime import datetime

from core.models import UserSubscription as UserSubModel
from user_subs.schemas import UserSubsBase, UserSubsResponse


async def get_users_subs(session: AsyncSession) -> list[UserSubModel]:
    stmt = select(UserSubModel).order_by(UserSubModel.id)
    result = await session.execute(stmt)
    return result.scalars().all()

async def get_subscriptions_by_user_id(session: AsyncSession, user_id: int) -> list[UserSubModel] | None:
    stmt = select(UserSubModel).where(user_id == UserSubModel.user_id)
    user_subs = await session.execute(stmt)
    return user_subs.scalars().all()

async def get_subscription_by_sub_and_user_id(session: AsyncSession, sub_id: int, user_id: int) -> UserSubModel | None:
    stmt = select(UserSubModel).where(user_id == UserSubModel.user_id and sub_id == UserSubModel.subscription_id)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()

async def add_user_sub(
        session: AsyncSession,
        user_sub_in: UserSubsBase
) -> UserSubModel:
    existing_sub = await session.execute(
        select(UserSubModel).where(user_sub_in.subscription_id == UserSubModel.subscription_id)
    )
    if existing_sub.scalar_one_or_none() is not None:
        raise HTTPException(
            status_code=400,
            detail="Subscription already exists"
        )

    subscription = UserSubModel(
        user_id=user_sub_in.user_id,
        subscription_id=user_sub_in.subscription_id,
        purchased_in=int(datetime.now().timestamp()),
    )

    session.add(subscription)
    await session.commit()
    await session.refresh(subscription)

    return subscription

async def delete_subscription(session: AsyncSession, subscription_id: int, user_id: int) -> UserSubsResponse | None:
    subscription = await get_subscription_by_sub_and_user_id(session, subscription_id, user_id)

    if subscription is None:
        raise HTTPException(
            status_code=404,
            detail="Subscription not found"
        )

    await session.delete(subscription)
    await session.commit()
    return subscription



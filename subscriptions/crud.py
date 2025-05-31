from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from datetime import datetime

from core.models import Subscription as SubscriptionModel
from subscriptions.schemas import SubscriptionBase, SubscriptionResponse


async def get_subscriptions(session: AsyncSession) -> list[SubscriptionModel]:
    stmt = select(SubscriptionModel).order_by(SubscriptionModel.id)
    result = await session.execute(stmt)
    return result.scalars().all()

async def get_subscription(session: AsyncSession, subscription_id: int) -> SubscriptionModel | None:
    subscription = await session.get(SubscriptionModel, subscription_id)
    return subscription

async def create_subscription(
        session: AsyncSession,
        subscription_in: SubscriptionBase
) -> SubscriptionModel:
    existing_subscription = await session.execute(
        select(SubscriptionModel).where(subscription_in.name == SubscriptionModel.name)
    )
    if existing_subscription.scalar_one_or_none() is not None:
        raise HTTPException(
            status_code=400,
            detail="Subscription already exists"
        )

    subscription = SubscriptionModel(
        name=subscription_in.name,
        cost=subscription_in.cost,
        duration=subscription_in.duration,
        access=subscription_in.access,
    )

    session.add(subscription)
    await session.commit()
    await session.refresh(subscription)

    return subscription

async def update_subscription(session: AsyncSession, subscription_id: int, new_subscription: SubscriptionBase) -> SubscriptionResponse | None:
    subscription = await get_subscription(session, subscription_id)
    if subscription:
        subscription.name = new_subscription.name
        subscription.cost = new_subscription.cost
        subscription.duration = new_subscription.duration
        subscription.access = new_subscription.access
    await session.commit()
    await session.refresh(subscription)
    return subscription

async def delete_subscription(session: AsyncSession, subscription_id) -> SubscriptionResponse | None:
    subscription = await get_subscription(session, subscription_id)

    if subscription is None:
        raise HTTPException(
            status_code=404,
            detail="Subscription not found"
        )

    await session.delete(subscription)
    await session.commit()
    return subscription



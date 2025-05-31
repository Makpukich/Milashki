from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from subscriptions.schemas import SubscriptionBase, SubscriptionResponse
from subscriptions.crud import get_subscription, get_subscriptions, create_subscription, update_subscription, \
    delete_subscription
from core.models import db_helper, Subscription

router = APIRouter(tags=["Subscriptions"])


@router.post("/subscriptions/", response_model=SubscriptionResponse)
async def create_new_subscription(
        subscription_in: SubscriptionBase,
        session: AsyncSession = Depends(db_helper.session_dependency),
):

    return await create_subscription(session, subscription_in)


@router.get("/subscriptions/", response_model=list[SubscriptionResponse])
async def read_subscriptions(
        session: AsyncSession = Depends(db_helper.session_dependency),
):

    return await get_subscriptions(session)


@router.get("/subscriptions/{subscription_id}", response_model=SubscriptionResponse)
async def read_subscription(
        subscription_id: int,
        session: AsyncSession = Depends(db_helper.session_dependency),
):

    subscription = await get_subscription(session, subscription_id)
    if subscription is None:
        raise HTTPException(status_code=404, detail="Subscription not found")
    return subscription


@router.put("/subscriptions/{subscription_id}", response_model=SubscriptionResponse)
async def update_existing_subscription(
        subscription_id: int,
        subscription_in: SubscriptionBase,
        session: AsyncSession = Depends(db_helper.session_dependency),
):

    subscription = await update_subscription(session, subscription_id, subscription_in)
    if subscription is None:
        raise HTTPException(status_code=404, detail="Subscription not found")
    return subscription


@router.delete("/subscriptions/{subscription_id}", response_model=SubscriptionResponse)
async def delete_existing_subscription(
        subscription_id: int,
        session: AsyncSession = Depends(db_helper.session_dependency)
):

    subscription = await delete_subscription(session, subscription_id)
    if subscription is None:
        raise HTTPException(status_code=404, detail="Subscription not found")
    return subscription
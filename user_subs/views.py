from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from user_subs.schemas import UserSubsBase, UserSubsResponse
from user_subs.crud import get_subscription_by_sub_and_user_id, get_users_subs, add_user_sub, delete_subscription, \
    get_subscriptions_by_user_id
from core.models import db_helper, UserSubscription

router = APIRouter(tags=["User_subs"])


@router.post("/User_subs/", response_model=UserSubsResponse)
async def add_subscription(
        subscription_in: UserSubsBase,
        session: AsyncSession = Depends(db_helper.session_dependency),
):

    return await add_user_sub(session, subscription_in)


@router.get("/User_subs/", response_model=list[UserSubsResponse])
async def read_all_subs(
        session: AsyncSession = Depends(db_helper.session_dependency),
):

    return await get_users_subs(session)

@router.get("/User_subs/{user_id}/{subscription_id}", response_model=UserSubsResponse)
async def read_subscription(
        subscription_id: int,
        user_id: int,
        session: AsyncSession = Depends(db_helper.session_dependency),
) -> UserSubsResponse:

    subscription = await get_subscription_by_sub_and_user_id(session, subscription_id, user_id)
    if subscription is None:
        raise HTTPException(status_code=404, detail="Subscription not found")
    return subscription

@router.get("/subscriptions/{user_id}", response_model=UserSubsResponse)
async def read_subscriptions(
        user_id: int,
        session: AsyncSession = Depends(db_helper.session_dependency),
):

    subscriptions = await get_subscriptions_by_user_id(session, user_id)
    if subscriptions is None:
        raise HTTPException(status_code=404, detail="Subscriptions not found")
    return subscriptions


@router.delete("/subscriptions/{user_id}/{sub_id}", response_model=UserSubsResponse)
async def delete_existing_subscription(
        user_id: int,
        subscription_id: int,
        session: AsyncSession = Depends(db_helper.session_dependency)
):

    subscription = await delete_subscription(session, subscription_id, user_id)
    if subscription is None:
        raise HTTPException(status_code=404, detail="Subscription not found")
    return subscription
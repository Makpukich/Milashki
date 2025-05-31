from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from core.models.db_helper import db_helper
from repositories.subscription_repo import SubscriptionPurchaseRepository
#from history.crud import get_purchase_by_id, get_purchases_by_wallet, pdate_purchase_subscription_type, delete_purchase
from history.schemas import SubscriptionResponse

router = APIRouter(tags=["Subscriptions"])


@router.get("/subscriptions/{purchase_id}", response_model=SubscriptionResponse)
async def read_subscription(
    purchase_id: int,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    """Получить подписку по ID"""
    repo = SubscriptionPurchaseRepository(session)
    subscription = await repo.get_purchase_by_id(purchase_id)
    if not subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")
    return subscription


@router.get("/wallets/{wallet_id}/subscriptions", response_model=list[SubscriptionResponse])
async def read_wallet_subscriptions(
    wallet_id: int,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    """Получить все подписки кошелька"""
    repo = SubscriptionPurchaseRepository(session)
    subscriptions = await repo.get_purchases_by_wallet(wallet_id)
    return subscriptions


@router.put("/subscriptions/{purchase_id}", response_model=SubscriptionResponse)
async def update_subscription_type(
    purchase_id: int,
    new_subscription_type_id: int,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    """Изменить тип подписки"""
    repo = SubscriptionPurchaseRepository(session)
    subscription = await repo.update_purchase_subscription_type(
        purchase_id=purchase_id,
        new_subscription_type_id=new_subscription_type_id
    )
    if not subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")
    return subscription


@router.delete("/subscriptions/{purchase_id}")
async def delete_subscription(
    purchase_id: int,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    """Удалить подписку"""
    repo = SubscriptionPurchaseRepository(session)
    success = await repo.delete_purchase(purchase_id)
    if not success:
        raise HTTPException(status_code=404, detail="Subscription not found")
    return {"message": "Subscription deleted successfully"}
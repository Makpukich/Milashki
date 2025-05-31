from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from repositories.subscription_repo import SubscriptionPurchaseRepository
from core.database import db_helper

router = APIRouter(prefix="/subscriptions", tags=["Subscriptions"])

@router.post("/purchases/")
async def create_purchase(
    wallet_id: int,
    subscription_type_id: int,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    repo = SubscriptionPurchaseRepository(session)
    purchase = await repo.add_purchase(wallet_id, subscription_type_id)
    return {"purchase_id": purchase.id}

@router.get("/purchases/wallet/{wallet_id}")
async def get_purchases_by_wallet(
    wallet_id: int,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    repo = SubscriptionPurchaseRepository(session)
    purchases = await repo.get_purchases_by_wallet(wallet_id)
    return {"purchases": [{
        "id": p.id,
        "subscription_type": p.subscription_type_id,
        "date": p.purchase_date.isoformat(),
    } for p in purchases]}
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from core.models.subscription import SubscriptionPurchase

class SubscriptionPurchaseRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_purchase(
        self,
        wallet_id: int,
        subscription_type_id: int,
        purchase_date: datetime | None = None,
    ) -> SubscriptionPurchase:
        purchase = SubscriptionPurchase(
            wallet_id=wallet_id,
            subscription_type_id=subscription_type_id,
            purchase_date=purchase_date or datetime.utcnow(),
        )
        self.session.add(purchase)
        await self.session.commit()
        return purchase

    async def get_purchase_by_id(self, purchase_id: int) -> SubscriptionPurchase | None:
        stmt = select(SubscriptionPurchase).where(SubscriptionPurchase.id == purchase_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_purchases_by_wallet(self, wallet_id: int) -> list[SubscriptionPurchase]:
        stmt = select(SubscriptionPurchase).where(SubscriptionPurchase.wallet_id == wallet_id)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def update_purchase_subscription_type(
        self,
        purchase_id: int,
        new_subscription_type_id: int,
    ) -> SubscriptionPurchase | None:
        stmt = (
            update(SubscriptionPurchase)
            .where(SubscriptionPurchase.id == purchase_id)
            .values(subscription_type_id=new_subscription_type_id)
            .returning(SubscriptionPurchase)
        )
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.scalar_one_or_none()

    async def delete_purchase(self, purchase_id: int) -> bool:
        stmt = delete(SubscriptionPurchase).where(SubscriptionPurchase.id == purchase_id)
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.rowcount > 0
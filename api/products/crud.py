from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from  sqlalchemy.engine import Result

from api.products.schemas import ProductCreate
from core.models import Product
async  def get_products(session: AsyncSession) -> list[Product]:
    stmt = select(Product).order_by(Product.id)
    result: Result = await session.execute(stmt)
    products = result.scalars().all()
    return list(products)

async def get_product(session: AsyncSession, product_id: int) -> Product | None:
    return await session.get(Product, product_id)

async def create_product(session: AsyncSession, product_in: ProductCreate) -> Product:
    product = Product(**product_in.model_dump())
    session.add(product)
    await session.commit()
    await session.refresh(product)
    return product
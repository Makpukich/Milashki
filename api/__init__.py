from fastapi import APIRouter

from .products.views import router as products_router
from .auth.views import router as auth_router
from .auth.auth import router as jwt_auth_router

auth_router.include_router(jwt_auth_router)

router = APIRouter()
router.include_router(router=products_router, prefix="/products")
router.include_router(router=auth_router)
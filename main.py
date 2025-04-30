
from contextlib import asynccontextmanager

from fastapi import FastAPI

import uvicorn

from core.config import settings
from api import router as router_v1
from core.models import db_helper, Base
from users.views import router as users_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router=router_v1, prefix=settings.api_prefix)
app.include_router(users_router)



if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)



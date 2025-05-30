
from contextlib import asynccontextmanager

from fastapi import FastAPI

import uvicorn

from core.config import settings
from api import router as router_v1
from core.models import db_helper, Base
from users.views import router as users_router

from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)
app.include_router(router=router_v1, prefix=settings.api_prefix)
app.include_router(users_router)



if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)



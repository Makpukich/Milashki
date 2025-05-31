from contextlib import asynccontextmanager
from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

from core.config import settings

from api import router as router_v1
from users.views import router as users_router
from subscriptions.views import router as sub_router
from user_subs.views import router as user_subs_router
from core.models import db_helper, Base

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router=router_v1)
app.include_router(users_router)
app.include_router(sub_router)
app.include_router(user_subs_router)



if __name__ == "__main__":
    uvicorn.run("main:app",reload=True)

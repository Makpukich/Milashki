from contextlib import asynccontextmanager

import uvicorn

from core.config import settings
from api import router as api_router
from core.models import Base, db_helper
from fastapi import FastAPI
from items import router as items_router

@asynccontextmanager
async  def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

app=FastAPI(lifespan=lifespan)
app.include_router(router=api_router, prefix=settings.api_prefix)
app.include_router(items_router)
@app.get("/")
def hello_world():
    return {
        "message" : "Hello world!",
    }

@app.get("/hello/{name}")
def hello(name):
    return {
        "message": f"hello {name}",
    }




if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)


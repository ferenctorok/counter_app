from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI

from counter_app import config as cfg
from counter_app.database import DBConnectionManager
from counter_app.router import counter_router


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None, None]:
    DBConnectionManager.init_with_postgresql_db(
        user=cfg.POSTGRES_USER,
        password=cfg.POSTGRES_PASSWORD,
        host=cfg.POSTGRES_HOST,
        port=cfg.POSTGRES_PORT,
        db_name=cfg.POSTGRES_DB,
    )
    yield


app = FastAPI(
    title="Counter Service",
    lifespan=lifespan,
    description="A simple API to manage a single integer counter",
    version="1.0.0",
    contact={"name": "Ferenc Török", "email": "ferenc.toeroek.bp@gmail.com"},
)

app.include_router(counter_router)

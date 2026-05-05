from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.routers import base, data
from app.core.config import get_settings
from motor.motor_asyncio import AsyncIOMotorClient


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.mongodb_client = AsyncIOMotorClient(get_settings().MONGODB_URL)
    app.database = app.mongodb_client[get_settings().MONGODB_DB_NAME]
    yield
    app.mongodb_client.close()

app = FastAPI(lifespan=lifespan)

app.include_router(base.router)
app.include_router(data.router)

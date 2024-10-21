import time
from fastapi import FastAPI
from contextlib import asynccontextmanager
import asyncio

from app.api.main import api_router

async def my_background_task():
    while True:
        await asyncio.sleep(1)
        print("hello")

@asynccontextmanager
async def lifespan(app: FastAPI):
    asyncio.create_task(my_background_task()())
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root( ):
    return {"message": "Hello World"}

app.include_router(api_router)


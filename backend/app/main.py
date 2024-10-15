import time
from fastapi import FastAPI
from contextlib import asynccontextmanager
import asyncio

from app.api.main import api_router


app = FastAPI()

class BackgroundRunner:
    def __init__(self):
        self.value = 0

    async def run_main(self):
        while True:
            await asyncio.sleep(0.1)
            print("message")

runner = BackgroundRunner()

@app.on_event('startup')
async def app_startup():
    asyncio.create_task(runner.run_main())

@app.get("/")
async def root( ):
    return {"message": "Hello World"}

app.include_router(api_router)


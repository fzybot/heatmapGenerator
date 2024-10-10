from fastapi import APIRouter

from app.api.routes import router_test

api_router = APIRouter()
api_router.include_router(router_test.router, prefix="/test", tags=["test"])
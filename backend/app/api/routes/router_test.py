from fastapi import APIRouter

router = APIRouter()
@router.get("/")
async def test_router():
    return {"message": "Hello from test router"}

@router.get("/inside_test")
async def inside_test_router():
    return {"message": "Hello from inside test router"}
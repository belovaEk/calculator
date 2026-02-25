from fastapi import APIRouter, Depends

router = APIRouter()

@router.post("/my_endpoint")
async def my_endpoint():
    return {"message": "Hello, World!"}

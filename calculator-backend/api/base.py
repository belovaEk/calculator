from fastapi import APIRouter
from api.v1 import calculate_route

api_router = APIRouter()
api_router.include_router(calculate_route.router, prefix="", tags=["Calculate_route"])
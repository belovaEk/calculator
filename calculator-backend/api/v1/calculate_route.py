from fastapi import APIRouter
from src.utils.calculate_util import calculate_util
from src.schemas.json_query_schema import JsonQuerySchema

router = APIRouter()

@router.post("/calculate")
async def calculate(data: JsonQuerySchema):
    result = await calculate_util(data=data)
    return result

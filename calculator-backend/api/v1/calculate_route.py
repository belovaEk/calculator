from fastapi import APIRouter
from src.utils.main_util import main_util
from src.schemas.json_query_schema import JsonQuerySchema

router = APIRouter()

@router.post("/calculate")
async def calculate(data: JsonQuerySchema):
    result = await main_util(data=data)
    return result

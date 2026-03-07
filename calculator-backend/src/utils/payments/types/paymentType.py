from ast import List
from typing import  Dict, TypeAlias
from src.schemas.json_query_schema import PeriodType
from src.schemas.json_query_schema import PeriodType
AmountByYear: TypeAlias = Dict[int, float]

class PeriodAmount(PeriodType):
    amount: float


PaymentsByYear: TypeAlias = Dict[int, List[PeriodAmount]]


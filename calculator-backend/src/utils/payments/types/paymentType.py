from ast import List
from typing import  Dict, TypeAlias
from src.schemas.json_query_schema import PeriodType, PensionCategoryRaw

AmountByYear: TypeAlias = Dict[int, float]

class PeriodAmount(PeriodType):
    amount: float
    type: PensionCategoryRaw


PaymentsByYear: TypeAlias = Dict[int, List[PeriodAmount]]


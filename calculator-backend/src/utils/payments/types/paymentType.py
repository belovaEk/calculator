from ast import List
from typing import  Dict, TypeAlias
from src.schemas.json_query_schema import PeriodType, PensionCategoryRaw

AmountByYear: TypeAlias = Dict[int, float]

class PeriodAmount(PeriodType):
    amount: float


class PaymentsByYearItem(PeriodAmount):
    type: PensionCategoryRaw
    periods: List[PeriodAmount]


PaymentsByYear: TypeAlias = Dict[int, PaymentsByYearItem]


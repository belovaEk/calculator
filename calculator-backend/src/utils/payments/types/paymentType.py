from typing import  Dict, TypeAlias
from src.schemas.json_query_schema import PeriodType

AmountByYear: TypeAlias = Dict[int, float]

PaymentsByYear: TypeAlias = Dict[int, Dict[PeriodType, float]]


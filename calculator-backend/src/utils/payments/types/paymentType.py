from typing import List
from typing import Dict, TypeAlias
from src.schemas.json_query_schema import PeriodType, PensionCategoryRaw
from pydantic import BaseModel

AmountByYear: TypeAlias = Dict[int, float]

class PeriodAmount(PeriodType):
    amount: float


class PaymentsByPeriodsItem(BaseModel):
    is_payment_transferred: bool
    type: PensionCategoryRaw  # "insurance_SPK", "social_SPK", "social_disability", "departmental"
    periods: List[PeriodAmount]  # [DN, DK, amount]


PaymentsByPeriods: TypeAlias = Dict[int, PaymentsByPeriodsItem]

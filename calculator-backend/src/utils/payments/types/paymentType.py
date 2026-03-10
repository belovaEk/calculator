from typing import List
from typing import Dict, TypeAlias
from src.schemas.json_query_schema import PeriodType, PensionCategoryRaw
from pydantic import BaseModel

AmountByYear: TypeAlias = Dict[int, float]

class PeriodAmount(PeriodType):
    amount: float

class PeriodAmountWithSP(PeriodAmount):
    sp_amount: float
    pmp_gss_amount: float


class PaymentsByPeriodsItem(BaseModel):
    is_payment_transferred: bool
    is_get_PSD_FSD_last_mounth_payment_trasferred: bool
    is_get_PSD_FSD_last_year_payment_trasferred: bool
    is_Not_get_PSD_FSD_now_payment_trasferred: bool

    type: PensionCategoryRaw  # "insurance_SPK", "social_SPK", "social_disability", "departmental"
    periods: List[PeriodAmount]  # [DN, DK, amount]


PaymentsByPeriods: TypeAlias = Dict[int, PaymentsByPeriodsItem]

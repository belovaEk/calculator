from typing import List, Optional
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
    is_payment_transferred: Optional[bool] = False
    is_get_PSD_FSD_last_mounth_payment_trasferred: Optional[bool] = False
    is_get_PSD_FSD_last_year_payment_trasferred: Optional[bool] = False
    is_Not_get_PSD_FSD_now_payment_trasferred: Optional[bool] = False

    type: Optional[PensionCategoryRaw] = None  # "insurance_SPK", "social_SPK", "social_disability", "departmental"
    periods: List[PeriodAmount]  # [DN, DK, amount]


PaymentsByPeriods: TypeAlias = Dict[int, PaymentsByPeriodsItem]

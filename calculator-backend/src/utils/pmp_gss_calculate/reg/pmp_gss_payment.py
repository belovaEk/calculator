from src.schemas.json_query_schema import (
    JsonQuerySchema,
    PeriodType,
    PeriodType,
    PaymentInterface,
)
from typing import List, Dict, TypeAlias

GssPmpPensionType: TypeAlias = Dict[int, List[PeriodType]]

from src.utils.pmp_gss_calculate.common.recalculation_pension_util import (
    recalculation_payment,
)


async def pmp_gss_pension(
    data: JsonQuerySchema, pmp_periods: List[PeriodType], gss_periods: List[PeriodType]
):
    """Функция пересчета ПМП и ГСС с учетом периодов пенсии"""

    pensions = [p for p in data.payments if p.type == "pension"]
    n = len(pensions)

    new_gss_periods: GssPmpPensionType = {}
    new_pmp_periods: GssPmpPensionType = {}
    
    new_pmp_periods = recalculation_payment(pensions=pensions, n=n, periods=pmp_periods)
    new_gss_periods = recalculation_payment(pensions=pensions, n=n, periods=gss_periods)

    return {"pmp_periods": new_pmp_periods, "gss_periods": new_gss_periods}

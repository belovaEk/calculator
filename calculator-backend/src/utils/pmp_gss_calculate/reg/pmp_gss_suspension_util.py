from src.schemas.json_query_schema import JsonQuerySchema, PeriodType, PeriodWithIdType
from typing import List

from src.utils.pmp_gss_calculate.common.recalculation_suspension_util import recalculation_suspension


async def pmp_gss_suspension(
    data: JsonQuerySchema, pmp_periods: List[PeriodType], gss_periods: List[PeriodType]
):
    """Функция для пересчета ГСС и ПМП с учетом периодов прерываний

    Args:
        data (JsonQuerySchema):
        pmp_periods (List[PeriodType]): периоды ПМП с учетом регистрации
        gss_periods (List[PeriodType]): периоды ГСС с учетом регистрации

    Returns:
        dict: Словарь с ключами
        - pmp_periods: List[PeriodType] - ПМП с учетом прерываний
        - gss_periods: List[PeriodType] - ГСС с учетом прерываний
    """
    periods_suspension = data.periods_suspension or None

    if periods_suspension:
        gss_periods = await recalculation_suspension(gss_periods, periods_suspension)
        pmp_periods = await recalculation_suspension(pmp_periods, periods_suspension)

    return {"pmp_periods": pmp_periods, "gss_periods": gss_periods}
from src.schemas.json_query_schema import JsonQuerySchema, PeriodType, PeriodWithIdType
from typing import List

from src.utils.pmp_gss_calculate.common.recalculation_suspension_util import recalculation_suspension


async def pmp_suspension(
    data: JsonQuerySchema, pmp_periods: List[PeriodType]
):
    """Функция для пересчета ПМП с учетом периодов прерываний

    Args:
        data (JsonQuerySchema):
        pmp_periods (List[PeriodType]): периоды ПМП

    Returns:
        dict: Словарь с ключами
        - pmp_periods: List[PeriodType] - ПМП с учетом прерываний
    """
    periods_suspension = data.periods_suspension or None

    if periods_suspension:

        pmp_periods = await recalculation_suspension(pmp_periods, periods_suspension)

    return {"pmp_periods": pmp_periods}

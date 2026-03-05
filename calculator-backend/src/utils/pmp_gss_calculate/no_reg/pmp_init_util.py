from typing import List
from src.schemas.json_query_schema import JsonQuerySchema, PeriodType

async def pmp_init(
    data: JsonQuerySchema,
    pmp_periods: List[PeriodType],
) -> dict:
    """
    Возвращает периоды ПМП по датам назначения пенсий

    Returns:
        dict: Словарь с ключами:
            - pmp_periods: List[PeriodType] - периоды, когда был назначен прожиточный минимум пенсионера (ПМП)

    {pmp_periods: [{'DN':DNpen, 'DK': DKpen}, {'DN':DNpen, 'DK': DKpen}]}
    """
    pensions = [p for p in data.payments if p.type == 'pension']

    for pension in pensions:
        pmp_periods.append(PeriodType(DN=pension.DN, DK=pension.DK))

    return {"pmp_periods": pmp_periods}
from typing import Dict, List
from datetime import date
from src.utils.pmp_gss_calculate.type import GssPmpPensionType, GssPmpIndexType


def split_periods_into_pairs_payment_amount(
    periods_data: GssPmpIndexType,
) -> Dict[str, Dict[int, dict]]:
    """
    Преобразует периоды из формата [[d1, d2, d3], [d4, d5]] в формат
    {
        "0": {
            0: {"DN": d1, "DK": d2, "amount": None},
            1: {"DN": d2, "DK": d3, "amount": None},
            2: {"DN": d4, "DK": d5, "amount": None}
        }
    }
    """
    result = {}

    for pension_id, period_lists in periods_data.items():
        pension_periods = []
        period_index = 0

        for date_list in period_lists:
            for i in range(len(date_list) - 1):
                pension_periods.append(
                    {"DN": date_list[i], "DK": date_list[i + 1], "amount": None}
                )

        result[pension_id] = pension_periods

    return result


async def pmp_gss_payment_amount(
    pmp_periods: GssPmpIndexType, gss_periods: GssPmpIndexType
) -> dict:
    """Функция преобразования индексированных периодов ПМП и ГСС в разрезанный формат"""

    split_pmp = split_periods_into_pairs_payment_amount(pmp_periods)
    split_gss = split_periods_into_pairs_payment_amount(gss_periods)

    return {"pmp_periods": split_pmp, "gss_periods": split_gss}

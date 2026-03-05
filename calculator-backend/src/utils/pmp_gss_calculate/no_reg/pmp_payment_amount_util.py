from typing import Dict, List
from datetime import date
from src.schemas.json_query_schema import PeriodWithIdType


from datetime import date
from src.schemas.json_query_schema import (
    JsonQuerySchema,
)
from src.utils.pmp_gss_calculate.common.process_payment_periods_util import process_payment_periods



async def pmp_payment_amount(
    pmp_periods: Dict[str, List[List[date]]],
    suspension_periods: List[PeriodWithIdType],
    data: JsonQuerySchema,
) -> dict:
    """
    Функция преобразования индексированных периодов ПМП и ГСС с расчетом amount
    """
    # Извлекаем все даты DK из suspension_periods для быстрого поиска
    suspension_dks = [p.DK for p in suspension_periods]
    
    # Обрабатываем оба типа периодов
    processed_pmp = await process_payment_periods(
        data,
        pmp_periods, 
        suspension_dks, 
        "pmp"
    )
    
    return {
        "pmp_periods": processed_pmp,
    }



# async def split_periods_into_pairs_payment_amount(
#     periods_data: GssPmpIndexType,
# ) -> Dict[str, Dict[int, dict]]:
#     """
#     Преобразует периоды из формата [[d1, d2, d3], [d4, d5]] в формат
#     {
#         "0": {
#             0: {"DN": d1, "DK": d2, "amount": None},
#             1: {"DN": d2, "DK": d3, "amount": None},
#             2: {"DN": d4, "DK": d5, "amount": None}
#         }
#     }
#     """
#     result = {}
#     for pension_id, period_lists in periods_data.items():
#         print(pension_id, period_lists)

#         pension_periods = []

#         for date_list in period_lists:
#             for i in range(len(date_list) - 1):
#                 pension_periods.append(
#                     {"DN": date_list[i], "DK": date_list[i + 1], "amount": None}
#                 )

#         result[pension_id] = pension_periods

#     return result


# async def pmp_gss_payment_amount(
#     pmp_periods: GssPmpIndexType, gss_periods: GssPmpIndexType
# ) -> dict:
#     """Функция преобразования индексированных периодов ПМП и ГСС в разрезанный формат"""

#     split_pmp = split_periods_into_pairs_payment_amount(pmp_periods)
#     split_gss = split_periods_into_pairs_payment_amount(gss_periods)

#     return {"pmp_periods": split_pmp, "gss_periods": split_gss}

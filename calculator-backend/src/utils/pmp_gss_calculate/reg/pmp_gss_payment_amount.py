from typing import Dict, List
from datetime import date
from src.schemas.json_query_schema import PeriodWithIdType
from src.utils.payments.pension_amount_util import calculate_sp_standart
from src.utils.payments.types.paymentType import (
    PaymentsByPeriods,
    PaymentsByPeriodsItem,
    PeriodAmount,
)

from datetime import date
from src.schemas.json_query_schema import (
    JsonQuerySchema,
)
from src.utils.pmp_gss_calculate.common.process_payment_periods_util import (
    process_payment_periods,
)
from src.utils.payments.types.paymentType import PeriodAmount
from src.utils.pmp_gss_calculate.type import GssPmpIndexType

from src.constants.gss_pmp_const import PMP_STANDART, GSS_STANDART


async def pmp_gss_payment_amount(
    pmp_periods: GssPmpIndexType,
    gss_periods: GssPmpIndexType,
    data: JsonQuerySchema,
) -> dict:
    """
    Функция преобразования индексированных периодов ПМП и ГСС с расчетом amount
    """
    suspension_periods = data.periods_suspension

    suspension_dks = [p.DK for p in suspension_periods]

    SP_STANDART: PaymentsByPeriods = await calculate_sp_standart(data)

    # SP_STANDART =
    #     0: {
    # 	    type: PensionCategoryRaw;
    # 	    periods: [
    #                   {DN, DK, amount};
    #                   {DN, DK, amount}
    #                 ]
    #     };
    #     1: {
    # 	    type: PensionCategoryRaw;
    # 	    periods: [
    #                   {DN, DK, amount};
    #                   {DN, DK, amount}
    #                 ]
    #     }
    # }

    for l in range(len(SP_STANDART)):
        if SP_STANDART[l].type == "social_disability":
            result = await social_disability(
                sp_standart_item=SP_STANDART[l], gss_periods=gss_periods
            )
        elif (
            SP_STANDART[l].type == "social_SPK"
            or SP_STANDART[l].type == "departmental"
            or SP_STANDART[l].type == "insurance_SPK"
        ):
            result = await social_SPK_insurance_SPK_departmental()
        else:
            print("Некорректно выбран тип пенсии")
            pass

    return result


async def social_disability(
    sp_standart_item: PaymentsByPeriodsItem, gss_periods: GssPmpIndexType
):

    gss_standart = GSS_STANDART

    # SP_STANDART = {
    # 0: {
    #     type: PensionCategoryRaw;
    #     periods: [
    #               {DN, DK, amount};
    #               {DN, DK, amount}
    #             ]
    # };
    #     1: {
    # 	    type: PensionCategoryRaw;
    # 	    periods: [
    #                   {DN, DK, amount};
    #                   {DN, DK, amount}
    #                 ]
    #     }
    # }

    # словарь вида {0: [{"DN": date, "DK": date, "amount": float}, ...]}
    gss_periods_with_amount = Dict[int, List[PeriodAmount]]

    for i in len(gss_periods):
        gss_periods_with_amount[i] = []
        for j in len(i):
            current_date = gss_periods[i][j]
            for d in len(sp_standart_item.periods):
                if (
                    i == 0
                    and j == 0
                    and sp_standart_item.is_payment_transferred
                    and current_date >= sp_standart_item.periods[0].DK
                ):
                    sp_year = sp_standart_item.periods[0].amount
                else:
                    m = len(sp_standart_item.periods)
                    if d == m - 1:
                        sp_year = 0
                    elif (
                        sp_standart_item.periods[d].DN
                        <= current_date
                        < sp_standart_item.periods[d].DK
                    ):
                        sp_year = sp_standart_item.periods[d].amount

            year = current_date.year
            if current_date.month == 12:
                amount = gss_standart[year] - sp_year
            else:
                amount = gss_standart[year + 1] - sp_year
        if j == 0 or amount > gss_periods_with_amount[i][j - 1].amount:
            gss_periods_with_amount[i].append(
                PeriodAmount(DN=current_date, DK=gss_periods[i][j + 1], amount=amount)
            )
        else:
            gss_periods_with_amount[i].append(
                PeriodAmount(
                    DN=current_date,
                    DK=gss_periods[i][j + 1],
                    amount=gss_periods_with_amount[i][j - 1].amount,
                )
            )


async def social_SPK_insurance_SPK_departmental():
    pass


# async def pmp_gss_payment_amount(
#     pmp_periods: Dict[str, List[List[date]]],
#     gss_periods: Dict[str, List[List[date]]],
#     data: JsonQuerySchema,
# ) -> dict:
#     """
#     Функция преобразования индексированных периодов ПМП и ГСС с расчетом amount
#     """
#     suspension_periods = data.periods_suspension
#     # Извлекаем все даты DK из suspension_periods для быстрого поиска
#     suspension_dks = [p.DK for p in suspension_periods]

#     # Обрабатываем оба типа периодов
#     processed_pmp = await process_payment_periods(
#         data,
#         pmp_periods,
#         suspension_dks,
#         "pmp"
#     )

#     processed_gss = await process_payment_periods(
#         data,
#         gss_periods,
#         suspension_dks,
#         "gss"
#     )

#     return {
#         "pmp_periods": processed_pmp,
#         "gss_periods": processed_gss
#     }


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
#             for l in range(len(date_list) - 1):
#                 pension_periods.append(
#                     {"DN": date_list[l], "DK": date_list[l + 1], "amount": None}
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

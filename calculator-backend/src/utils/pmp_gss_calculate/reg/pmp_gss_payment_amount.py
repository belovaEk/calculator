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


import logging

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,  # Уровень: DEBUG, INFO, WARNING, ERROR, CRITICAL
    format="%(asctime)s - %(levelname)s - %(message)s",  # Формат: время - уровень - сообщение
    handlers=[logging.StreamHandler()],  # Вывод в консоль
)

async def pmp_gss_payment_amount(
    pmp_periods: GssPmpIndexType,
    gss_periods: GssPmpIndexType,
    data: JsonQuerySchema,
) -> dict:
    """
    Функция преобразования индексированных периодов ПМП и ГСС с расчетом amount
    """
    try: 
        suspension_periods = data.periods_suspension
        suspension_dks = [p.DK for p in suspension_periods]
    except:
        suspension_periods = []

    SP_STANDART: PaymentsByPeriods = await calculate_sp_standart(data)
    # logging.info(f"Весь SP_STANDART: {SP_STANDART}")
    
    # Инициализируем результирующие словари
    result_pmp_periods: Dict[int, List] = {}
    result_gss_periods: Dict[int, List] = {}

    for l in range(len(SP_STANDART)):
        if SP_STANDART[l].type == "social_disability":
            result = await social_disability(
                sp_standart_item=SP_STANDART[l], 
                gss_periods=gss_periods[l],
            )
            # social_disability возвращает {"pmp_periods": [], "gss_periods": [...]}
            result_pmp_periods[l] = result["pmp_periods"]
            result_gss_periods[l] = result["gss_periods"]
            
        elif (
            SP_STANDART[l].type == "social_SPK"
            or SP_STANDART[l].type == "departmental"
            or SP_STANDART[l].type == "insurance_SPK"
        ):
            result = await social_SPK_insurance_SPK_departmental(
                sp_standart_item=SP_STANDART[l],
                gss_periods=gss_periods[l],
                pmp_periods=pmp_periods[l],
                suspension_dks=suspension_dks,
            )
            # social_SPK_insurance_SPK_departmental возвращает {"pmp_periods": [...], "gss_periods": [...]}
            result_pmp_periods[l] = result["pmp_periods"]
            result_gss_periods[l] = result["gss_periods"]
        else:
            print("Некорректно выбран тип пенсии")
            # Инициализируем пустыми списками для некорректных типов
            result_pmp_periods[l] = []
            result_gss_periods[l] = []

    return {
        "pmp_periods": result_pmp_periods,
        "gss_periods": result_gss_periods
    }

async def social_disability(
    sp_standart_item: PaymentsByPeriodsItem, 
    gss_periods: GssPmpIndexType,
):

    gss_standart = GSS_STANDART

    # SP_STANDART = {
    # 0: {
    #     is_payment_transferred: bool
    #     type: PensionCategoryRaw;
    #     periods: [
    #               {DN, DK, amount};
    #               {DN, DK, amount}
    #             ]
    # };
    #     1: {
    #     is_payment_transferred: bool
    # 	    type: PensionCategoryRaw;
    # 	    periods: [
    #                   {DN, DK, amount};
    #                   {DN, DK, amount}
    #                 ]
    #     }
    # }

    # словарь вида {0: [{"DN": date, "DK": date, "amount": float}, ...]}
    gss_periods_with_amount: List[PeriodAmount] = []


    for i in range(len(gss_periods)):
        for j in range(len(gss_periods[i])-1):
            current_date = gss_periods[i][j]
            for d in range(len(sp_standart_item.periods)):
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
                        <= sp_standart_item.periods[d].DK
                    ):
                        sp_year = sp_standart_item.periods[d].amount
                        break

            year = current_date.year
            if current_date.month == 12:
                amount = gss_standart[year+1] - sp_year
            else:
                amount = gss_standart[year + 1] - sp_year
            if j == 0 or amount > gss_periods_with_amount[j - 1].amount:
                gss_periods_with_amount.append(
                    PeriodAmount(DN=current_date, DK=gss_periods[i][j + 1], amount=round(amount, 2))
                )
            else:
                gss_periods_with_amount.append(
                    PeriodAmount(
                        DN=current_date,
                        DK=gss_periods[i][j + 1],
                        amount=round(gss_periods_with_amount[j - 1].amount, 2),
                    )
                )

    
    return {
        'pmp_periods': [],
        'gss_periods': gss_periods_with_amount
    }




async def recalculation_gss_amount(
    sp_standart_item,
    gss_periods,
    gss_standart,
    ):
    
    # SP_STANDART = {
    # 0: {
    #     is_payment_transferred: bool
    #     type: PensionCategoryRaw;
    #     periods: [
    #               {DN, DK, amount};
    #               {DN, DK, amount}
    #             ]
    # };
    #     1: {
    #     is_payment_transferred: bool
    # 	    type: PensionCategoryRaw;
    # 	    periods: [
    #                   {DN, DK, amount};
    #                   {DN, DK, amount}
    #                 ]
    #     }
    # }

    # словарь вида {0: [{"DN": date, "DK": date, "amount": float}, ...]}
    gss_periods_with_amount: List[PeriodAmount] = []

    for i in range(len(gss_periods)):
        for j in range(len(gss_periods[i])-1):
            current_date = gss_periods[i][j]
            for d in range(len(sp_standart_item.periods)):
                m = len(sp_standart_item.periods)
                if (
                    sp_standart_item.periods[d].DN
                    <= current_date
                    < sp_standart_item.periods[d].DK
                ):
                    # Дата попала в период d
                    if d < m - 1:  # если есть следующий период
                        sp_year = sp_standart_item.periods[d].amount
                        sp_year_plus_one = sp_standart_item.periods[d+1].amount
                        break
                    else:  # последний период
                        sp_year = 0
                        sp_year_plus_one = 0
                        break
                else:
                    sp_year = 0
                    sp_year_plus_one = 0

            year = current_date.year
            if current_date.month == 12:
                amount = gss_standart[year+1] - sp_year_plus_one
            else:
                amount = gss_standart[year] - sp_year
            if j == 0 or amount > gss_periods_with_amount[j - 1].amount:
                gss_periods_with_amount.append(
                    PeriodAmount(DN=current_date, DK=gss_periods[i][j + 1], amount=round(amount, 2))
                )
            else:
                gss_periods_with_amount.append(
                    PeriodAmount(
                        DN=current_date,
                        DK=gss_periods[i][j + 1],
                        amount=round(gss_periods_with_amount[j - 1].amount, 2),
                    )
                )
    return gss_periods_with_amount


async def recalculation_pmp_amount(
    sp_standart_item,
    pmp_periods,
    pmp_standart,
    suspension_dks,
    ):
    # SP_STANDART = {
    # 0: {
    #     is_payment_transferred: bool
    #     type: PensionCategoryRaw;
    #     periods: [
    #               {DN, DK, amount};
    #               {DN, DK, amount}
    #             ]
    # };
    #     1: {
    #     is_payment_transferred: bool
    # 	    type: PensionCategoryRaw;
    # 	    periods: [
    #                   {DN, DK, amount};
    #                   {DN, DK, amount}
    #                 ]
    #     }
    # }

    # словарь вида {0: [{"DN": date, "DK": date, "amount": float}, ...]}
    pmp_periods_with_amount: List[PeriodAmount] = [] 

    for i in range(len(pmp_periods)):
        for j in range(len(pmp_periods[i])-1):
            current_date = pmp_periods[i][j]
            for d in range(len(sp_standart_item.periods)):
                if (
                    i == 0
                    and j == 0
                    and sp_standart_item.is_payment_transferred
                    and current_date >= sp_standart_item.periods[0].DK
                ):
                    sp_year = sp_year_minus_one = sp_standart_item.periods[0].amount
                else:
                    m = len(sp_standart_item.periods)
                    if d == m - 1:
                        sp_year = 0
                        sp_year_minus_one = 0
                    elif (
                        sp_standart_item.periods[d].DN
                        <= current_date
                        <= sp_standart_item.periods[d].DK
                    ):
                        sp_year = sp_standart_item.periods[d].amount
                        sp_year_minus_one = sp_standart_item.periods[d-1].amount
                    

            year = current_date.year
            if current_date.month == 12:
                amount = pmp_standart[year+1] - sp_year
            else:
                # Логика проверки на даты возобновлений
                for k in range(len(suspension_dks)):
                    if current_date == suspension_dks[k]:
                        amount = pmp_standart[year] - sp_year_minus_one
                        break
                    if k == len(suspension_dks) - 1: 
                        amount = pmp_standart[year] - sp_year
                amount = pmp_standart[year + 1] - sp_year
            if j == 0 or amount > pmp_periods_with_amount[j - 1].amount:
                pmp_periods_with_amount.append(
                    PeriodAmount(DN=current_date, DK=pmp_periods[i][j + 1], amount=round(amount, 2))
                )
            else:
                pmp_periods_with_amount.append(
                    PeriodAmount(
                        DN=current_date,
                        DK=pmp_periods[i][j + 1],
                        amount=round(pmp_periods_with_amount[j - 1].amount, 2),
                    )
                )
    return pmp_periods_with_amount

async def social_SPK_insurance_SPK_departmental(
    sp_standart_item: PaymentsByPeriodsItem,
    gss_periods: GssPmpIndexType,
    pmp_periods: GssPmpIndexType,
    suspension_dks,
    ):

    gss_standart = GSS_STANDART
    pmp_standart = PMP_STANDART

    pmp_periods_amount = await recalculation_pmp_amount(
        sp_standart_item=sp_standart_item,
        pmp_periods=pmp_periods,
        pmp_standart=pmp_standart,
        suspension_dks=suspension_dks,
        )
    
    gss_periods_amount = await recalculation_gss_amount(
        sp_standart_item=sp_standart_item,
        gss_periods=gss_periods,
        gss_standart=gss_standart,
        ) 

    return {
        'pmp_periods': pmp_periods_amount,
        'gss_periods': gss_periods_amount
    }


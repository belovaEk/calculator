from src.utils.pmp_gss_calculate.type import GssPmpIndexType
from src.utils.payments.pension_amount_util import calculate_sp_standart
from src.utils.pmp_gss_calculate.common.breakpoint_utils import split_pmp_periods_by_breakpoints, get_breakpoints_date

from src.schemas.json_query_schema import JsonQuerySchema
from src.utils.payments.types.paymentType import (
    PaymentsByPeriods,
    PeriodAmount,
    PeriodAmountWithSP,
)
from typing import List, Dict
from dateutil.relativedelta import relativedelta
from datetime import date


def calculate_rsd_for_period(
    period: PeriodAmount,
    sp_standart_periods: List,
    data_poiska_pensii: date
) -> tuple:
    """
    Расчет РСД для периода на основе даты поиска пенсии
    
    Returns:
        tuple: (sp_amount, rsd_amount)
    """
    sp_amount = 0.0
    
    for sp_period in sp_standart_periods:
        if sp_period.DN <= data_poiska_pensii < sp_period.DK:
            sp_amount = round(sp_period.amount, 2)
            break
    
    # Если SP не найден, пробуем следующий месяц
    if sp_amount == 0:
        next_month = (data_poiska_pensii.replace(day=1) + relativedelta(months=1))
        for sp_period in sp_standart_periods:
            if sp_period.DN <= next_month < sp_period.DK:
                sp_amount = round(sp_period.amount, 2)
                break
    
    rsd_amount = round(period.amount - sp_amount, 2)
    return sp_amount, rsd_amount


def apply_previous_rsd_if_less(
    current_rsd: float,
    previous_rsd: float,
    period: PeriodAmount,
    sp_amount: float
) -> PeriodAmountWithSP:
    """
    Применяет правило: если текущий РСД меньше предыдущего, используем предыдущий
    """
    final_rsd = previous_rsd if current_rsd < previous_rsd else current_rsd
    
    return PeriodAmountWithSP(
        DN=period.DN,
        DK=period.DK,
        amount=final_rsd,
        sp_amount=sp_amount,
        pmp_gss_amount=round(period.amount, 2),
    )


async def alt_pmp_gss_payment_amount(
    pmp_periods: Dict[int, List[PeriodAmount]],
    gss_periods: Dict[int, List[PeriodAmount]],
    data: JsonQuerySchema
) -> Dict[str, Dict[int, List[PeriodAmountWithSP]]]:

    if not (data.periods_suspension):
        suspension_periods = []
    else:
        suspension_periods = data.periods_suspension    

    if not (data.periods_inpatient):
        periods_inpatient = []
    else:
        periods_inpatient = data.periods_inpatient  

    sp_standart: PaymentsByPeriods = await calculate_sp_standart(data)

    result_pmp: Dict[int, List[PeriodAmountWithSP]] = {}
    result_gss: Dict[int, List[PeriodAmountWithSP]] = {}

    # Формируем массив breakpoints в котором будут лежать даты смена категории пенсии:
    breakpoints = await get_breakpoints_date(data=data)

    # Получаем периоды ПМП и ГСС, разбитые по датам из breakpoints
    pmp_periods = split_pmp_periods_by_breakpoints(pmp_or_gss_periods=pmp_periods, breakpoints=breakpoints)
    gss_periods = split_pmp_periods_by_breakpoints(pmp_or_gss_periods=gss_periods, breakpoints=breakpoints)

    # Обработка ПМП
    for l in range(len(pmp_periods)):
        result_pmp.setdefault(l, [])

        for j in range(len(pmp_periods[l])):
            current_period = pmp_periods[l][j]
            data_poiska_pensii = None
            
            # Определяем дату поиска пенсии
            if j == 0:
                # Первый период
                if len(gss_periods[l]) >= 1 and current_period.DN < gss_periods[l][0].DN:
                    if sp_standart[l].is_payment_transferred:
                        if (sp_standart[l].is_get_PSD_FSD_last_mounth_payment_trasferred
                            and sp_standart[l].is_get_PSD_FSD_last_year_payment_trasferred):
                            
                            if sp_standart[l].is_Not_get_PSD_FSD_now_payment_trasferred:
                                data_poiska_pensii = date(current_period.DN.year - 1, 12, 1)
                            else:
                                # РСД = 0
                                result_pmp[l].append(
                                    PeriodAmountWithSP(
                                        DN=current_period.DN,
                                        DK=current_period.DK,
                                        amount=0.0,
                                        sp_amount=0.0,
                                        pmp_gss_amount=round(current_period.amount, 2),
                                    )
                                )
                                continue
                        else:
                            data_poiska_pensii = current_period.DN
                    else:
                        data_poiska_pensii = current_period.DN
                else:
                    data_poiska_pensii = current_period.DN - relativedelta(months=1)
                    
                    # Проверка периодов приостановки
                    for k in range(len(suspension_periods)):
                        if current_period.DN == suspension_periods[k].DK and k >= 1:
                            data_poiska_pensii = date(data.periods_suspension[k].DN.year - 1, 12, 1)
                            break
                    
                    # Проверка периодов стационара
                    for m in range(len(periods_inpatient)):
                        check_date = (periods_inpatient[m].DN + relativedelta(months=1)).replace(day=1)
                        if current_period.DN == check_date:
                            data_poiska_pensii = date(data.periods_inpatient[m].DN.year - 1, 12, 1)
                            break
            else:
                # Не первый период
                data_poiska_pensii = current_period.DN - relativedelta(months=1)
                
                # Проверка периодов приостановки
                for k in range(len(suspension_periods)):
                    if current_period.DN == suspension_periods[k].DK and k >= 1:
                        data_poiska_pensii = date(data.periods_suspension[k].DN.year - 1, 12, 1)
                        break
                
                # Проверка периодов стационара
                for m in range(len(periods_inpatient)):
                    check_date = (periods_inpatient[m].DN + relativedelta(months=1)).replace(day=1)
                    if current_period.DN == check_date:
                        data_poiska_pensii = date(data.periods_inpatient[m].DN.year - 1, 12, 1)
                        break
                
                # Проверка breakpoints
                for k in range(len(breakpoints)):
                    if current_period.DN == breakpoints[k]:
                        data_poiska_pensii = breakpoints[k]
                        break
                
                # Увеличиваем на месяц для поиска SP
                data_poiska_pensii = (data_poiska_pensii.replace(day=1) + relativedelta(months=1))
            
            # Расчет SP и РСД
            sp_amount, rsd_amount = calculate_rsd_for_period(
                current_period,
                sp_standart[l].periods,
                data_poiska_pensii
            )
            
            # Добавление результата с учетом предыдущего периода
            if j == 0:
                result_pmp[l].append(
                    PeriodAmountWithSP(
                        DN=current_period.DN,
                        DK=current_period.DK,
                        amount=rsd_amount,
                        sp_amount=sp_amount,
                        pmp_gss_amount=round(current_period.amount, 2),
                    )
                )
            else:
                prev_rsd = result_pmp[l][j - 1].amount
                result_pmp[l].append(
                    apply_previous_rsd_if_less(
                        rsd_amount,
                        prev_rsd,
                        current_period,
                        sp_amount
                    )
                )
    
    # Обработка ГСС
    for l in range(len(gss_periods)):
        result_gss.setdefault(l, [])
        
        for j in range(len(gss_periods[l])):
            current_period = gss_periods[l][j]
            
            # Определяем дату поиска пенсии
            data_poiska_pensii = current_period.DN
            
            # Проверка breakpoints
            for k in range(len(breakpoints)):
                if current_period.DN == breakpoints[k]:
                    data_poiska_pensii = breakpoints[k]
                    break
            
            # Расчет SP и РСД
            sp_amount, rsd_amount = calculate_rsd_for_period(
                current_period,
                sp_standart[l].periods,
                data_poiska_pensii
            )
            
            # Добавление результата с учетом предыдущего периода
            if j == 0:
                result_gss[l].append(
                    PeriodAmountWithSP(
                        DN=current_period.DN,
                        DK=current_period.DK,
                        amount=rsd_amount,
                        sp_amount=sp_amount,
                        pmp_gss_amount=round(current_period.amount, 2),
                    )
                )
            else:
                prev_rsd = result_gss[l][j - 1].amount
                result_gss[l].append(
                    apply_previous_rsd_if_less(
                        rsd_amount,
                        prev_rsd,
                        current_period,
                        sp_amount
                    )
                )
    
    return {"pmp_periods": result_pmp, "gss_periods": result_gss}
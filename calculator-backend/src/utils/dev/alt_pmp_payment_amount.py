from src.utils.pmp_gss_calculate.type import GssPmpIndexType
from src.utils.payments.pension_amount_util import calculate_sp_standart
from src.schemas.json_query_schema import JsonQuerySchema
from src.utils.payments.types.paymentType import (
    PaymentsByPeriods,
    PeriodAmount,
    PeriodAmountWithSP,
)
from typing import List, Dict
from dateutil.relativedelta import relativedelta
from datetime import date

from src.utils.pmp_gss_calculate.common.breakpoint_utils import split_pmp_periods_by_breakpoints, get_breakpoints_date

# Импортируем общие функции из alt_pmp_gss_payment_amount
from src.utils.dev.alt_pmp_gss_payment_amount import (
    calculate_rsd_for_period,
    apply_previous_rsd_if_less
)


async def alt_pmp_payment_amount(
    pmp_periods: Dict[int, List[PeriodAmount]],
    data: JsonQuerySchema,
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

    # Формируем массив breakpoints в котором будут лежать даты смена категории пенсии:
    breakpoints = await get_breakpoints_date(data=data)

    # Получаем периоды ПМП разбитые по датам из breakpoints
    pmp_periods = split_pmp_periods_by_breakpoints(pmp_or_gss_periods=pmp_periods, breakpoints=breakpoints)
    for l in range(len(pmp_periods)):
        result_pmp.setdefault(l, [])

        for j in range(len(pmp_periods[l])):
            current_period = pmp_periods[l][j]
            data_poiska_pensii = None
            
            # Определяем дату поиска пенсии
            if j == 0:
                # Первый период
                data_poiska_pensii = current_period.DN
                
                if sp_standart[l].is_payment_transferred:
                    if (sp_standart[l].is_get_PSD_FSD_last_mounth_payment_trasferred
                        and sp_standart[l].is_get_PSD_FSD_last_year_payment_trasferred):
                        
                        if sp_standart[l].is_Not_get_PSD_FSD_now_payment_trasferred:
                            data_poiska_pensii = current_period.DN - relativedelta(months=1)
                        else:
                            # Ветка "РСД до ПМП = 0": создаём запись с amount = 0
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
                    # else: data_poiska_pensii уже установлен как current_period.DN
                # else: data_poiska_pensii уже установлен как current_period.DN
                
            else:
                # Не первый период
                if current_period.DN != date(2022, 6, 1):
                    data_poiska_pensii = date(current_period.DN.year - 1, 12, 1)
                else:
                    data_poiska_pensii = current_period.DN
                
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
            
            # Расчет SP и РСД с использованием общей функции
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
                # Получаем РСД предыдущего периода
                prev_rsd = result_pmp[l][j - 1].amount
                
                # Используем общую функцию для сравнения с предыдущим периодом
                result_pmp[l].append(
                    apply_previous_rsd_if_less(
                        rsd_amount,
                        prev_rsd,
                        current_period,
                        sp_amount
                    )
                )

    return {"pmp_periods": result_pmp}
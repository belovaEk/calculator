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


    for l in range(len(pmp_periods)):
        result_pmp.setdefault(l, [])

        # Для ПМП
        for j in range(len(pmp_periods[l])):
            sp_amount = 0  # Инициализация по умолчанию
            # По блок-схеме для j==0 базовая дата поиска = дата начала периода,
            # для остальных периодов (j>0) — дата начала периода минус 1 месяц (если не найдено возобновление).
            if j == 0:
                if len(gss_periods[l]) >= 1 and pmp_periods[l][j].DN < gss_periods[l][0].DN:
                    if sp_standart[l].is_payment_transferred:
                        if (sp_standart[l].is_get_PSD_FSD_last_mounth_payment_trasferred
                            and sp_standart[l].is_get_PSD_FSD_last_year_payment_trasferred):
                            
                            if sp_standart[l].is_Not_get_PSD_FSD_now_payment_trasferred:
                                #
                                data_poiska_pensii = date(pmp_periods[l][j].DN.year - 1, 12, 1)

                            else:
                                # Ветка "РСД до ПМП = 0": создаём запись с amount = 0 и переходим к следующему периоду
                                result_pmp[l].append(
                                    PeriodAmountWithSP(
                                        DN=pmp_periods[l][j].DN,
                                        DK=pmp_periods[l][j].DK,
                                        amount=0.0,
                                        sp_amount=0.0,
                                        pmp_gss_amount=round(pmp_periods[l][j].amount, 2),
                                    )
                                )
                                continue
                        else:
                            data_poiska_pensii = pmp_periods[l][j].DN
                    else: # необходимо добавить иначе у вас получается когда отрабатывает условие False, то data_poiska_pensii не записывается
                        data_poiska_pensii = pmp_periods[l][j].DN #data_poiska_pensii = 01.08.2025 
                else:
                    data_poiska_pensii = pmp_periods[l][j].DN - relativedelta(months=1) #data_poiska_pensii = 12.07.2025 - 1 month = 12.06.2025
                    for k in range(len(suspension_periods)): #0
                        if pmp_periods[l][j].DN == suspension_periods[k].DK and k >= 1:
                            # дата поиска = дата приостановки (k-1) - 1 месяц
                            data_poiska_pensii = date(data.periods_suspension[k].DN.year - 1, 12, 1)
                            break
                    for m in range(len(periods_inpatient)): #1
                        if pmp_periods[l][j].DN == (periods_inpatient[m].DN+ relativedelta(months=1)).replace(day=1): #01.08.2025 == 01.08.2025
                             # дата поиска = (год(дата попадания в стационар (m))) - 1 год) 1 декабря
                            data_poiska_pensii = date(data.periods_inpatient[m].DN.year - 1, 12, 1) #01.12.2024
                            break

            # j != 0
            else:
                data_poiska_pensii = pmp_periods[l][j].DN - relativedelta(months=1)
                for k in range(len(suspension_periods)):
                    if pmp_periods[l][j].DN == suspension_periods[k].DK and k >= 1:
                        # дата поиска = (год(дата начала приостановки (k)) - 1 год) 1 декабря
                        data_poiska_pensii = date(data.periods_suspension[k].DN.year - 1, 12, 1)
                        break
                    #добавляем проверку на совпадение с периодами попадания в стационар
                for m in range(len(periods_inpatient)):
                    if pmp_periods[l][j].DN == (periods_inpatient[m].DN+ relativedelta(months=1)).replace(day=1):
                        # дата поиска = (год(дата попадания в стационар (m))) - 1 год) 1 декабря
                        data_poiska_pensii = date(data.periods_inpatient[m].DN.year - 1, 12, 1)
                        break

                for k in range(len(breakpoints)):
                    if pmp_periods[l][j].DN == breakpoints[k]:
                        data_poiska_pensii = breakpoints[k]
                        for period in sp_standart[l].periods:
                            if period.DN <= data_poiska_pensii < period.DK:
                                sp_amount = round(period.amount, 2)
                                break
                            amount = round(pmp_periods[l][j].amount - sp_amount, 2)
                            result_pmp[l].append(
                                PeriodAmountWithSP(
                                    DN=pmp_periods[l][j].DN,
                                    DK=pmp_periods[l][j].DK,
                                    amount=amount,
                                    sp_amount=sp_amount,
                                    pmp_gss_amount=round(pmp_periods[l][j].amount, 2),
                                )
                            )
                            break

                data_poiska_pensii = (data_poiska_pensii.replace(day=1) + relativedelta(months=1))
                
            # Поиск подходящего sp_standart периода
            for period in sp_standart[l].periods:
                if period.DN <= data_poiska_pensii < period.DK:
                    sp_amount = round(period.amount, 2)
                    break
                
            if sp_amount==0:
                data_poiska_pensii = (data_poiska_pensii.replace(day=1) + relativedelta(months=1))
                for period in sp_standart[l].periods:
                    if period.DN <= data_poiska_pensii < period.DK:
                        sp_amount = round(period.amount, 2)
                        break
            
            amount = round(pmp_periods[l][j].amount - sp_amount, 2)

            if j == 0:
                result_pmp[l].append(
                    PeriodAmountWithSP(
                        DN=pmp_periods[l][j].DN,
                        DK=pmp_periods[l][j].DK,
                        amount=amount,
                        sp_amount=sp_amount,
                        pmp_gss_amount=round(pmp_periods[l][j].amount, 2),
                    )
                )
            else:
                # Получаем РСД предыдущего периода
                prev_rsd = result_pmp[l][j - 1].amount
                
                # Если текущий РСД меньше предыдущего, используем предыдущий РСД
                if amount < prev_rsd:
                    result_pmp[l].append(
                        PeriodAmountWithSP(
                            DN=pmp_periods[l][j].DN,
                            DK=pmp_periods[l][j].DK,
                            amount=prev_rsd,  # ← используем предыдущий РСД
                            sp_amount=sp_amount,
                            pmp_gss_amount=round(pmp_periods[l][j].amount, 2),  # ← текущая сумма ПМП
                        )
                    )
                else:
                    result_pmp[l].append(
                        PeriodAmountWithSP(
                            DN=pmp_periods[l][j].DN,
                            DK=pmp_periods[l][j].DK,
                            amount=amount,
                            sp_amount=sp_amount,
                            pmp_gss_amount=round(pmp_periods[l][j].amount, 2),
                        )
                    )

        # Для ГСС
        result_gss.setdefault(l, [])
        for j in range(len(gss_periods[l])):
            sp_amount = 0
            is_breakpoint_processed = False  # Флаг, что период уже обработан через breakpoint
            
            # Проверка на breakpoint
            for k in range(len(breakpoints)):
                if gss_periods[l][j].DN == breakpoints[k]:
                    data_poiska_pensii = breakpoints[k]
                    for period in sp_standart[l].periods:
                        if period.DN <= data_poiska_pensii < period.DK:
                            sp_amount = round(period.amount, 2)
                            break
                        else:
                            # ВАЖНО: этот блок else относится к for period
                            # Нужно пересмотреть логику
                            pass
                    
                    # Если нашли sp_amount, рассчитываем и добавляем
                    if sp_amount > 0 or True:  # Уточните условие
                        amount = round(gss_periods[l][j].amount - sp_amount, 2)
                        result_gss[l].append(
                            PeriodAmountWithSP(
                                DN=gss_periods[l][j].DN,
                                DK=gss_periods[l][j].DK,
                                amount=amount,
                                sp_amount=sp_amount,
                                pmp_gss_amount=round(gss_periods[l][j].amount, 2),
                            )
                        )
                        is_breakpoint_processed = True
                        break  # Выходим из цикла по breakpoints
            
            # Если период не был обработан через breakpoint, используем основную логику
            if not is_breakpoint_processed:
                data_poiska_pensii = gss_periods[l][j].DN
                
                for period in sp_standart[l].periods:
                    if period.DN <= data_poiska_pensii < period.DK:
                        sp_amount = round(period.amount, 2)
                        break
                
                current_rsd = round(gss_periods[l][j].amount - sp_amount, 2)
                
                # Логика сравнения с предыдущим периодом
                if j == 0:
                    result_gss[l].append(
                        PeriodAmountWithSP(
                            DN=gss_periods[l][j].DN,
                            DK=gss_periods[l][j].DK,
                            amount=current_rsd,
                            sp_amount=sp_amount,
                            pmp_gss_amount=round(gss_periods[l][j].amount, 2),
                        )
                    )
                else:
                    prev_rsd = result_gss[l][j - 1].amount
                    if current_rsd < prev_rsd:
                        result_gss[l].append(
                            PeriodAmountWithSP(
                                DN=gss_periods[l][j].DN,
                                DK=gss_periods[l][j].DK,
                                amount=prev_rsd,
                                sp_amount=sp_amount,
                                pmp_gss_amount=round(gss_periods[l][j].amount, 2),
                            )
                        )
                    else:
                        result_gss[l].append(
                            PeriodAmountWithSP(
                                DN=gss_periods[l][j].DN,
                                DK=gss_periods[l][j].DK,
                                amount=current_rsd,
                                sp_amount=sp_amount,
                                pmp_gss_amount=round(gss_periods[l][j].amount, 2),
                            )
                        )

    return {"pmp_periods": result_pmp, "gss_periods": result_gss}

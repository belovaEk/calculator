from src.utils.pmp_gss_calculate.type import GssPmpPensionType

from src.utils.pmp_gss_calculate.common.recalculation_date_index_util import recalculation_date_index

from src.constants.gss_pmp_const import GSS_STANDART, PMP_STANDART
from src.utils.payments.types.paymentType import PeriodAmount
from typing import Dict, List
from datetime import date
from dateutil.relativedelta import relativedelta

async def pmp_gss_index (pmp_periods: GssPmpPensionType, gss_periods: GssPmpPensionType, reg: bool):

    """ Функция пересчета ПМП и ГСС на периоды индексации и нахождение принадлежащим к этим периодам стандратам выплат

    Returns:
        Словари с индексами пенсий и их периодами + стандартные выплаты к этим периодам: 
        pmp_periods: {
            0: {
            [DN: 2020-02-02, DK: 2021-01-01, amount: pmp_standart для этого периода],
            [DN: 2020-02-02, DK: 2021-01-01, amount: pmp_standart для этого периода]
            }
    """    

    new_pmp_periods = await period_index_calculate(periods=pmp_periods, period_standards=PMP_STANDART)

    if reg:
        
        new_gss_periods = await period_index_calculate(periods=gss_periods, period_standards=GSS_STANDART) 

        return {
            'pmp_periods': new_pmp_periods,
            'gss_periods': new_gss_periods
        }
    
    else:
        return {
            'pmp_periods': new_pmp_periods,
        }



async def period_index_calculate (periods: GssPmpPensionType, period_standards: Dict[date, float]) -> Dict[int, List[PeriodAmount]]:
    """ Функция пересчета ПМП или ГСС на периоды индексации и нахождение принадлежащим к этим периодам стандратам выплат

    Args:
        periods (GssPmpPensionType): периоды ГСС или ПМП обработаанные после регистраций, приостановок и стационаризаций
        period_stanadrts (List[date, float]): ПМП стандарт или ГСС стандарт (константы)
    Returns:
        Dict[int, List[PeriodAmount]]: периоды пмп или гсс:
        pmp_periods: {
            0: {
            [DN: 2020-02-02, DK: 2021-01-01, amount: pmp_standart для этого периода],
            [DN: 2020-02-02, DK: 2021-01-01, amount: pmp_standart для этого периода]
            }
    """    
    result_periods: Dict[int, List[PeriodAmount]] = {}
    
    # Сортируем стандарты по дате
    sorted_standards = sorted(period_standards.items())

    if len(periods) == 0:
        return result_periods
    
    for pension_idx, pension_periods in periods.items():
        result_periods[pension_idx] = []
        
        for period in pension_periods:

            # Находим все даты индексации, попадающие в период
            relevant_standards = [
                (idx, date, amount) 
                for idx, (date, amount) in enumerate(sorted_standards)
                if date <= period.DK
            ]
            
            if not relevant_standards:
                continue
                
            # Берем первую дату индексации, которая >= началу периода
            start_idx = 0
            for i, (_, idx_date, _) in enumerate(relevant_standards):
                if idx_date <= period.DN:
                    start_idx = i
            
            current_date = period.DN
            

            for i in range(start_idx, len(relevant_standards)):
                _, index_date, amount = relevant_standards[i]
                
                # Определяем конец текущего периода индексации
                if i + 1 < len(relevant_standards):
                    next_index_date = relevant_standards[i + 1][1]
                    period_end = min(period.DK, next_index_date - relativedelta(days=1))
                else:
                    period_end = period.DK
                
                # Корректируем начало, если оно раньше даты индексации
                start = max(current_date, index_date)
                
                if start <= period_end:
                    result_periods[pension_idx].append(PeriodAmount(
                        DN=start,
                        DK=period_end,
                        amount=amount
                    ))
                    current_date = period_end + relativedelta(days=1)
    
    return result_periods
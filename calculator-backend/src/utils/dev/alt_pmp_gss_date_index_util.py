from src.utils.pmp_gss_calculate.type import GssPmpPensionType

from src.utils.pmp_gss_calculate.common.recalculation_date_index_util import recalculation_date_index

from src.constants.gss_pmp_const import GSS_STANDART, PMP_STANDART
from src.utils.payments.types.paymentType import PeriodAmount
from typing import Dict, List
from datetime import date
from dateutil.relativedelta import relativedelta
from src.schemas.json_query_schema import JsonQuerySchema

async def pmp_gss_index (pmp_periods: GssPmpPensionType, gss_periods: GssPmpPensionType, reg: bool, data: JsonQuerySchema):

    """ Функция пересчета ПМП и ГСС на периоды индексации и нахождение принадлежащим к этим периодам стандратам выплат

    Returns:
        Словари с индексами пенсий и их периодами + стандартные выплаты к этим периодам: 
        pmp_periods: {
            0: {
            [DN: 2020-02-02, DK: 2021-01-01, amount: pmp_standart для этого периода],
            [DN: 2020-02-02, DK: 2021-01-01, amount: pmp_standart для этого периода]
            }
    """    

    new_pmp_periods = await period_index_calculate(periods=pmp_periods, period_standards=PMP_STANDART, data=data)
  
    if reg:
        
        new_gss_periods = await period_index_calculate(periods=gss_periods, period_standards=GSS_STANDART, data=data) 
        
        return {
            'pmp_periods': new_pmp_periods,
            'gss_periods': new_gss_periods
        }
    
    else:
        return {
            'pmp_periods': new_pmp_periods,
        }



async def period_index_calculate(
    periods: GssPmpPensionType, 
    period_standards: Dict[date, float],
    data: JsonQuerySchema
) -> Dict[int, List[PeriodAmount]]:
    """ 
    Функция пересчета ПМП или ГСС на периоды индексации и нахождение принадлежащим к этим периодам стандартам выплат
    
    Args:
        periods (GssPmpPensionType): периоды ГСС или ПМП обработанные после регистраций, приостановок и стационаризаций
        period_standards (Dict[date, float]): ПМП стандарт или ГСС стандарт (константы)
        last_pension_end_date (Optional[date]): Дата окончания последней пенсии. Если указана, периоды обрезаются до этой даты
        
    Returns:
        Dict[int, List[PeriodAmount]]: периоды пмп или гсс
    """    
    result_periods: Dict[int, List[PeriodAmount]] = {}
    
    # Сортируем стандарты по дате
    sorted_standards = sorted(period_standards.items())

    last_pension_end_date = None
    if data.payments:
        pension_end_dates = [
            payment.DK for payment in data.payments 
            if payment.type == "pension"
            ]
        if pension_end_dates:
            last_pension_end_date = max(pension_end_dates)
            print(f"Last pension end date: {last_pension_end_date}")
    
    if len(periods) == 0:
        return result_periods
    
    for pension_idx, pension_periods in periods.items():
        result_periods[pension_idx] = []
        
        for period in pension_periods:
            # Обрезаем период по дате окончания последней пенсии
            DN = period.DN
            DK = period.DK
            
            if last_pension_end_date:
                # Если период полностью после последней пенсии - пропускаем
                if DN >= last_pension_end_date:
                    print(f"Skipping period {pension_idx} from {DN} to {DK} (starts after last pension end date {last_pension_end_date})")
                    continue
                
                # Если период выходит за последнюю пенсию - обрезаем
                if DK > last_pension_end_date:
                    DK = last_pension_end_date
                    print(f"Truncating period {pension_idx} from {period.DK} to {DK}")
                    
                    # Если после обрезания дата начала >= дате окончания - пропускаем
                    if DN >= DK:
                        print(f"Skipping truncated period {pension_idx} (DN={DN} >= DK={DK})")
                        continue
            
            # Находим все даты индексации, попадающие в период
            relevant_standards = [
                (idx, date, amount) 
                for idx, (date, amount) in enumerate(sorted_standards)
                if date <= DK  # Используем обрезанную DK
            ]
            
            if not relevant_standards:
                continue
                
            # Берем первую дату индексации, которая >= началу периода
            start_idx = 0
            for i, (_, idx_date, _) in enumerate(relevant_standards):
                if idx_date <= DN:
                    start_idx = i
            
            current_date = DN
            

            for i in range(start_idx, len(relevant_standards)):
                _, index_date, amount = relevant_standards[i]
                                
                # Определяем конец текущего периода индексации
                if i + 1 < len(relevant_standards):
                    next_index_date = relevant_standards[i + 1][1]
                    period_end = min(DK, next_index_date - relativedelta(days=1))
                else:
                    period_end = DK
                
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
from src.schemas.json_query_schema import JsonQuerySchema, PeriodType, PaymentInterface
from datetime import date
from dateutil.relativedelta import relativedelta
from typing import List


async def PMP_GSS_primal(dr10: date, spv_init_date: date, list_of_periods_reg: List[PeriodType], PMP: List[PeriodType], GSS: List[PeriodType]) -> dict:
    """
    Возвращает ПМП и ГСС в зависимости от ДР10 и ДатыПервойСПВ
    
    Returns:
        dict: Словарь с ключами:
            - PMP: List[PeriodType] - периоды, когда был назначен прожиточный минимум пенсионера (ПМП)
            - GSS: List[PeriodType] - периоды, когда был назначен городской социальный стандарт (ГСС)

    {PMP: [{'DN':DNreg, 'DK': DKreg}, {'DN':DNreg, 'DK': DKreg}], 
    GSS: [{'DN':DNreg, 'DK': DKreg}, {'DN':DNreg, 'DK': DKreg}]}
    """

    if dr10 < spv_init_date:
        return await dr10_earlier(spv_init_date, list_of_periods_reg, PMP, GSS)
    else:
        return await spv_init_date_earlier(dr10, spv_init_date, list_of_periods_reg, PMP, GSS)
    
    
async def spv_init_date_earlier(dr10: date, spv_init_date: date, list_of_periods_reg: List[PeriodType], PMP: List[PeriodType], GSS: List[PeriodType]) -> dict:
    """
    Обрабатывает случай, когда дата первой СПВ раньше даты достижения 10 лет регистрации
    
    Returns:
        dict: Словарь с ключами:
            - PMP: List[PeriodType] - периоды, когда был назначен прожиточный минимум пенсионера (ПМП)
            - GSS: List[PeriodType] - периоды, когда был назначен городской социальный стандарт (ГСС)
    """
    i = 0
    n = len(list_of_periods_reg)
    
    currentDate = date.today()
    
    PMP.append({'DN': spv_init_date, 'DK': dr10})
    
    while i < n:
        
        DKreg = list_of_periods_reg[i].DK
        DNreg = list_of_periods_reg[i].DN
        
        if DKreg >= dr10 >= DNreg:
            if i == n-1:
                GSS.append({'DN':dr10, 'DK':DKreg})
                if DKreg != currentDate:
                    PMP.append({'DN': DKreg, 'DK': currentDate})
            else:
                GSS.append({'DN':dr10, 'DK': DKreg})
                PMP.append({'DN': DKreg, 'DK': list_of_periods_reg[i+1].DN})
                
        elif DNreg > dr10 and DKreg > dr10:
            if i == n-1:
                GSS.append({'DN': DNreg, 'DK': DKreg})
                if DKreg != currentDate:
                    PMP.append({'DN': DKreg, 'DK':currentDate})
            else:
                GSS.append({'DN':DNreg, 'DK': DKreg})
                PMP.append({'DN':DKreg, 'DK': list_of_periods_reg[i+1].DN})
        i+=1

    return {'PMP': PMP, 'GSS': GSS}
    

            
async def dr10_earlier(spv_init_date: date, list_of_periods_reg: List[PeriodType], PMP: List[PeriodType], GSS: List[PeriodType]) -> dict:
    """
    Обрабатывает случай, когда дата достижения 10 лет регистрации раньше даты первой СПВ
    
    Returns:
        dict: Словарь с ключами:
            - PMP: List[PeriodType] - периоды, когда был назначен прожиточный минимум пенсионера (ПМП)
            - GSS: List[PeriodType] - периоды, когда был назначен городской социальный стандарт (ГСС)

    """
    i = 0
    n = len(list_of_periods_reg)
    
    currentDate = date.today()
    
    while i < n - 1:
        
        DKreg = list_of_periods_reg[i].DK
        DNreg = list_of_periods_reg[i].DN
        
        if DKreg > spv_init_date >= DNreg:
            if i == n-1:
                GSS.append({'DN':spv_init_date, 'DK': DKreg})
                if DKreg != currentDate:
                    PMP.append({'DN':DKreg, 'DK': currentDate})
            else:
                GSS.append({'DN':spv_init_date, 'DK': DKreg})
                PMP.append({'DN':DKreg, 'DK': list_of_periods_reg[i+1].DN})
                
        elif DKreg <= spv_init_date < list_of_periods_reg[i+1].DN :

            if i == n-1:
                PMP.append({'DN':spv_init_date, 'DK': currentDate})
            else:
                PMP.append({'DN':spv_init_date, 'DK': DNreg})
                
        elif spv_init_date < DNreg < DKreg:

            if i == n-1:
                GSS.append({'DN':DNreg, 'DK': DKreg})
                if DKreg != currentDate:
                    PMP.append({'DN':DKreg, 'DK': currentDate})
            else:
                GSS.append({'DN':DNreg, 'DK': DKreg})
                PMP.append({'DN':DKreg, 'DK': list_of_periods_reg[i+1].DN})
        i+=1

    return {'PMP': PMP, 'GSS': GSS}


def sort_periods_in_data(data: JsonQuerySchema) -> JsonQuerySchema:
    """
    Сортирует периоды регистрации в Москве по дате начала (DN) внутри структуры data.
    Сортирует поля: periods_reg_moscow, periods_reg_representative_moscow, periods_reg_breadwinner_moscow
    """
    # Сортируем периоды регистрации ребенка
    if data.periods_reg_moscow:
        data.periods_reg_moscow = sorted(
            data.periods_reg_moscow, 
            key=lambda period: period.DN
        )
    
    # Сортируем периоды регистрации законного представителя
    if data.periods_reg_representative_moscow:
        data.periods_reg_representative_moscow = sorted(
            data.periods_reg_representative_moscow, 
            key=lambda period: period.DN
        )
    
    # Сортируем периоды регистрации кормильца
    if data.periods_reg_breadwinner_moscow:
        data.periods_reg_breadwinner_moscow = sorted(
            data.periods_reg_breadwinner_moscow, 
            key=lambda period: period.DN
        )
    
    return data
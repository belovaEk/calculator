from src.schemas.json_query_schema import JsonQuerySchema, PeriodType, PaymentInterface
from datetime import date
from dateutil.relativedelta import relativedelta
from typing import List


async def PMP_GSS_primal(dr10: date, spv_init_date: date, list_of_periods_reg: List[PeriodType], PMP: List[PeriodType], GSS: List[PeriodType]) -> dict:
    """
    Возвращает ПМП и ГСС в зависимости от ДР10 и ДатыПервойСПВ
    """
    if dr10 < spv_init_date:
        return dr10_earlier(spv_init_date, list_of_periods_reg, PMP, GSS)
    else:
        return spv_init_date_earlier(dr10, spv_init_date, list_of_periods_reg, PMP, GSS)
    
    
async def spv_init_date_earlier(dr10: date, spv_init_date: date, list_of_periods_reg: List[PeriodType], PMP: List[PeriodType], GSS: List[PeriodType]) -> dict:
    i = 0
    n = len(list_of_periods_reg)
    
    currentDate = date.today()
    
    PMP.append([spv_init_date, dr10])
    
    while i < n:
        
        DKreg = list_of_periods_reg[i].DK
        DNreg = list_of_periods_reg[i].DN
        
        if DKreg >= dr10 >= DNreg:
            if i == n-1:
                GSS.append([dr10, DKreg])
                if DKreg != currentDate:
                    PMP.append([DKreg, currentDate])
            else:
                GSS.append([dr10, DKreg])
                PMP.append([DKreg, list_of_periods_reg[i+1].DN])
                
        elif DNreg > dr10 and DKreg > dr10:
            if i == n-1:
                GSS.append([DNreg, DKreg])
                if DKreg != currentDate:
                    PMP.append([DKreg, currentDate])
            else:
                GSS.append([DNreg, DKreg])
                PMP.append([DKreg, list_of_periods_reg[i+1].DN])
        i+=1
    
    return {'PMP': PMP, 'GSS': GSS}
    

            
async def dr10_earlier(spv_init_date: date, list_of_periods_reg: List[PeriodType], PMP: List[PeriodType], GSS: List[PeriodType]) -> dict:
    i = 0
    n = len(list_of_periods_reg)
    
    currentDate = date.today()
    
    while i < n:
        
        DKreg = list_of_periods_reg[i].DK
        DNreg = list_of_periods_reg[i].DN
        
        if DKreg > spv_init_date >= DNreg:
            if i == n-1:
                GSS.append([spv_init_date, DKreg])
                if DKreg != currentDate:
                    PMP.append([DKreg, currentDate])
            else:
                GSS.append([spv_init_date, DKreg])
                PMP.append([DKreg, list_of_periods_reg[i+1].DN])
                
        elif DKreg <= spv_init_date < list_of_periods_reg[i+1].DN :
            if i == n-1:
                PMP.append([spv_init_date, currentDate])
            else:
                PMP.append([spv_init_date, DNreg])
                
        elif spv_init_date < DNreg < DKreg:
            if i == n-1:
                GSS.append([DNreg, DKreg])
                if DKreg != currentDate:
                    PMP.append([DKreg, currentDate])
            else:
                GSS.append([DNreg, DKreg])
                PMP.append([DKreg, list_of_periods_reg[i+1].DN])
        i+=1
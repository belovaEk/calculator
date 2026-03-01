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
    
    while i <= n - 1:
        
        DKreg = list_of_periods_reg[i].DK
        DNreg = list_of_periods_reg[i].DN
        
        if DKreg >= dr10 >= DNreg:
            if i == n-1:
                GSS.append(PeriodType(DN=dr10, DK=DKreg))
                if DKreg != currentDate:
                    PMP.append(PeriodType(DN=DKreg, DK=currentDate))
            else:
                GSS.append(PeriodType(DN=dr10, DK=DKreg))
                PMP.append(PeriodType(DN=DKreg, DK=list_of_periods_reg[i+1].DN))
                
        elif DNreg > dr10 and DKreg > dr10:
            if i == n-1:
                GSS.append(PeriodType(DN=DNreg, DK=DKreg))
                if DKreg != currentDate:
                    PMP.append(PeriodType(DN=DKreg, DK=currentDate))
            else:
                GSS.append(PeriodType(DN=DNreg, DK=DKreg))
                PMP.append(PeriodType(DN=DKreg, DK=list_of_periods_reg[i+1].DN))
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
    
    while i <= n - 1:
        DKreg = list_of_periods_reg[i].DK
        DNreg = list_of_periods_reg[i].DN
        
        if DKreg > spv_init_date >= DNreg:
            if i == n-1:
                GSS.append(PeriodType(DN=spv_init_date, DK=DKreg))
                if DKreg != currentDate:
                     PMP.append(PeriodType(DN=DKreg, DK=currentDate))
            else:
                GSS.append(PeriodType(DN=spv_init_date, DK=DKreg))
                PMP.append(PeriodType(DN=DKreg, DK=list_of_periods_reg[i+1].DN))
                
        elif DKreg <= spv_init_date < list_of_periods_reg[i+1].DN :

            if i == n-1:
                PMP.append(PeriodType(DN=spv_init_date, DK=currentDate))
            else:
                PMP.append(PeriodType(DN=spv_init_date, DK=DNreg))
                
        elif spv_init_date < DNreg < DKreg:

            if i == n-1:
                GSS.append(PeriodType(DN=DNreg, DK=DKreg))
                if DKreg != currentDate:
                    PMP.append(PeriodType(DN=DKreg, DK=currentDate))
            else:
                GSS.append(PeriodType(DN=DNreg, DK=DKreg))
                PMP.append(PeriodType(DN=DKreg, DK=list_of_periods_reg[i+1].DN))
        i+=1

    return {'PMP': PMP, 'GSS': GSS}


def sort_periods_in_data(data: JsonQuerySchema) -> JsonQuerySchema:
    """
    Сортирует периоды регистрации в Москве по дате начала (DN) внутри структуры data.
    Сортирует поля: periods_reg_moscow, periods_reg_representative_moscow, periods_reg_breadwinner_moscow,  periods_suspension, periods_inpatient
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
        
    if data.periods_suspension:
        data.periods_suspension = sorted(
            data.periods_suspension, 
            key=lambda period: period.DN
        )
        
    if data.periods_inpatient:
        data.periods_inpatient = sorted(
            data.periods_inpatient, 
            key=lambda period: period.DN
        )
    
    return data




def PMP_GSS_suspension(data: JsonQuerySchema, pmp_periods: List[PeriodType], gss_periods: List[PeriodType]):
    
    periods_suspension = data.periods_suspension or None
    
    if periods_suspension is not None:
        
        current_gss: List[PeriodType] = gss_periods.copy()
        
        for suspension in periods_suspension:
            
            new_gss: List[PeriodType] = []
            
            DNsus = suspension.DN # дата приостановки
            DKsus = suspension.DK # дата возобновления

            for gss in current_gss:
                
                DNgss = gss.DN # дата начала ГСС
                DKgss = gss.DK # дата конца ГСС
                
                # Если дата приостановки пенсии попала между датами выплаты ГСС
                if DNgss < DNsus and DKgss < DKsus: 
                    new_gss.append(PeriodType(DN=DNgss, DK=DNsus))
                    
                # Еcли между датами периода выплат ГСС попадает дата возобновления выплаты пенсии
                elif DNsus < DNgss < DKsus < DKgss:
                    new_gss.append(PeriodType(DN=DKsus, DK=DKgss))
                    
                # Если период выплаты ГСС у нас попадает между двумя датами приостановки и возобновления пенсии
                elif DNsus < DNgss < DKgss < DKsus:
                    continue
                    
                # Если даты приостановки и возобновления наоборот попадают внутрь периода выплат ГСС
                elif DNgss < DNsus < DKsus < DKgss:
                    new_gss.append(PeriodType(DN=DNgss, DK=DNsus))
                    new_gss.append(PeriodType(DN=DKsus, DK=DKgss))
                  
                # Если не подпал под условия добавляем исходный период 
                else:
                    new_gss.append(gss)
                    
            current_gss = new_gss # обновляем для следующей итерации
            
        gss_periods[:] = current_gss  # заменяем исходный список
                    
                
               
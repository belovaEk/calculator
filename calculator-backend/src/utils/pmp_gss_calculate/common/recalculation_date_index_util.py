from src.utils.pmp_gss_calculate.type import GssPmpPensionType, GssPmpIndexType
from datetime import date
from typing import Optional
from src.schemas.json_query_schema import JsonQuerySchema

def recalculation_date_index(
    pensions: GssPmpPensionType, 
    data: JsonQuerySchema,
) -> GssPmpIndexType:
    """
    Создает индексы дат для периодов, обрезая их по дате окончания последней пенсии
    
    Args:
        pensions: Словарь периодов ПМП/ГСС
        last_pension_end_date: Дата окончания последней пенсии (если указана, периоды обрезаются)
    """
    new_periods: GssPmpIndexType = {}

    last_pension_end_date = None
    if data.payments:
        pension_end_dates = [
            payment.DK for payment in data.payments 
            if payment.type == "pension"
            ]
        if pension_end_dates:
            last_pension_end_date = max(pension_end_dates)
            print(f"Last pension end date: {last_pension_end_date}")

    for index, periods in pensions.items():
        new_periods[index] = []
        
        for period_num, period in enumerate(periods):
            new_periods[index].append([])

            DN = period.DN
            DK = period.DK
            
            # Обрезаем дату окончания, если указана последняя дата пенсии
            if last_pension_end_date and DK > last_pension_end_date:
                DK = last_pension_end_date
                print(f"Truncating period {index}:{period_num} from {period.DK} to {DK}")
            
            # Если после обрезания дата начала больше или равна дате окончания - пропускаем период
            if DN >= DK:
                print(f"Skipping period {index}:{period_num} because DN ({DN}) >= DK ({DK})")
                continue
            
            current_date = DN
            
            # Добавляем начальную дату
            new_periods[index][period_num].append(current_date)
            
            # Генерируем все 31 декабря между DN и DK
            year = current_date.year
            while date(year, 12, 31) < DK:
                dec_31 = date(year, 12, 31)
                if dec_31 > current_date:  # Не добавляем, если это та же дата
                    new_periods[index][period_num].append(dec_31)
                year += 1
            
            # Добавляем конечную дату, если она не 31 декабря и не равна начальной
            if DK not in new_periods[index][period_num] and DK > DN:
                new_periods[index][period_num].append(DK)
    
    return new_periods
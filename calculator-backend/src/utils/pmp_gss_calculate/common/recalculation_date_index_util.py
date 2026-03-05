from src.utils.pmp_gss_calculate.type import GssPmpPensionType, GssPmpIndexType
from datetime import date



def recalculation_date_index(pensions: GssPmpPensionType) -> GssPmpIndexType:

    new_periods: GssPmpIndexType = {}

    for index, periods in pensions.items():
        new_periods[index] = []
        
        for period_num, period in enumerate(periods):
            new_periods[index].append([])

            DN = period.DN
            DK = period.DK
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
            
            # Добавляем конечную дату, если она не 31 декабря
            if DK not in new_periods[index][period_num]:
                new_periods[index][period_num].append(DK)
    
    return new_periods
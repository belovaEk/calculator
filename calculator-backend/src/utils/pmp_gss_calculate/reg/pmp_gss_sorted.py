from typing import Dict, List
from datetime import date
from src.utils.payments.types.paymentType import PeriodAmount

async def pmp_gss_sorted(
    pmp_periods: Dict[int, List[PeriodAmount]],
    gss_periods: Dict[int, List[PeriodAmount]]
) -> Dict[int, List[dict]]:
    """
    Объединяет pmp и gss периоды по pension_id, добавляет поле pmp_or_gss и сортирует по DN
    """
    result: Dict[int, List[dict]] = {}
    
    # Получаем все уникальные pension_id из обоих словарей
    all_pension_ids = set(pmp_periods.keys()) | set(gss_periods.keys())
    
    for pension_id in all_pension_ids:
        combined_periods = []
        
        # Добавляем PMP периоды с пометкой
        if pension_id in pmp_periods:
            for period in pmp_periods[pension_id]:
                period_dict = period.dict() if hasattr(period, 'dict') else dict(period)
                period_dict["pmp_or_gss"] = "ПМП"
                combined_periods.append(period_dict)
        
        # Добавляем GSS периоды с пометкой
        if pension_id in gss_periods:
            for period in gss_periods[pension_id]:
                period_dict = period.dict() if hasattr(period, 'dict') else dict(period)
                period_dict["pmp_or_gss"] = "ГСС"
                combined_periods.append(period_dict)
        
        # Сортируем по DN
        combined_periods.sort(key=lambda x: x["DN"])
        
        result[pension_id] = combined_periods
    
    return result
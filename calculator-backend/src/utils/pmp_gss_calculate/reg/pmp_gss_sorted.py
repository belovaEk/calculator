from typing import Dict, List, Optional
from datetime import date
from src.utils.payments.types.paymentType import PeriodAmount
from src.schemas.json_query_schema import JsonQuerySchema

async def pmp_gss_sorted(
    pmp_periods: Dict[int, List[PeriodAmount]],
    gss_periods: Dict[int, List[PeriodAmount]],
    data: JsonQuerySchema,
) -> Dict[int, List[dict]]:
    """
    Объединяет pmp и gss периоды по pension_id, добавляет поле pmp_or_gss и сортирует по DN
    
    Args:
        pmp_periods: Словарь периодов ПМП
        gss_periods: Словарь периодов ГСС
        last_pension_end_date: Если указана, удаляет периоды, начинающиеся после этой даты
    """
    result: Dict[int, List[dict]] = {}
    
    # Получаем все уникальные pension_id из обоих словарей
    all_pension_ids = set(pmp_periods.keys()) | set(gss_periods.keys())
    
    last_pension_end_date = None
    if data.payments:
        pension_end_dates = [
            payment.DK for payment in data.payments 
            if payment.type == "pension"
            ]
        if pension_end_dates:
            last_pension_end_date = max(pension_end_dates)
            print(f"Last pension end date: {last_pension_end_date}")

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
        
        # Фильтруем периоды, которые начинаются после последней даты пенсии
        if last_pension_end_date:
            filtered_periods = []
            for period in combined_periods:
                period_start = period.get("DN")
                if period_start is None:
                    print(f"Warning: period has None DN, skipping: {period}")
                    continue
                if period_start < last_pension_end_date:
                    filtered_periods.append(period)
                else:
                    print(f"Removing period starting at {period_start} (after last pension end date {last_pension_end_date})")
            combined_periods = filtered_periods
        
        # Сортируем по DN (только если есть периоды)
        if combined_periods:
            combined_periods.sort(key=lambda x: x["DN"])
        
        result[pension_id] = combined_periods
    
    return result
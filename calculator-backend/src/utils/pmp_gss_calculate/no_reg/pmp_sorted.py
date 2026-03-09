from typing import Dict, List
from datetime import date
from src.utils.payments.types.paymentType import PeriodAmount

async def pmp_sorted(
    pmp_periods: Dict[int, List[PeriodAmount]]
) -> Dict[int, List[dict]]:
    """
    Принимает pmp периоды по pension_id, добавляет поле pmp_or_gss и сортирует по DN
    """
    result: Dict[int, List[dict]] = {}
    
    for pension_id, periods in pmp_periods.items():
        combined_periods = []
        
        for period in periods:
            period_dict = period.dict() if hasattr(period, 'dict') else dict(period)
            period_dict["pmp_or_gss"] = "ПМП"
            combined_periods.append(period_dict)
        
        # Сортируем по DN
        combined_periods.sort(key=lambda x: x["DN"])
        
        result[pension_id] = combined_periods
    
    return result
from typing import Dict, List
from datetime import date
from src.constants.gss_pmp_const import PMP_STANDART, GSS_STANDART
from src.utils.payments.types.paymentType import PaymentsByYear

from datetime import date
from typing import Dict, List, Optional
from src.utils.payments.pension_amount_util import pension_insurance_SPK_amount
from src.schemas.json_query_schema import (
    JsonQuerySchema,
)


def calculate_amount_for_period(
    start_date: date,
    end_date: date,
    suspension_dks: List[date],
    standart_dict: Dict[int, float],
    pension_id: int,
    SP_STANDART: PaymentsByYear,
    prev_amount: Optional[float] = None,
) -> float:
    """Вычисляет amount для одного периода"""
    
    year = start_date.year
    
    # Определяем базовое значение по алгоритму
    if start_date.month == 12:
        # Случай А: месяц = 12
        amount = standart_dict[year + 1] - SP_STANDART[pension_id][year]
    else:
        # Случай Б: месяц != 12
        if start_date in suspension_dks:
            # Дата есть в suspension
            amount = standart_dict[year] - SP_STANDART[pension_id][year - 1]
        else:
            # Даты нет в suspension
            amount = standart_dict[year] - SP_STANDART[pension_id][year]
    
    # Корректировка по предыдущему значению
    if prev_amount is not None and amount <= prev_amount:
        amount = prev_amount
    
    return round(amount, 2)


async def process_payment_periods(
    data: JsonQuerySchema,
    periods_data: Dict[str, List[List[date]]],
    suspension_dks: List[date],
    period_type: str  # "pmp" или "gss"
) -> Dict[str, List[dict]]:
    """
    Обрабатывает периоды для одного типа (PMP или GSS)
    
    Args:
        periods_data: словарь вида {"0": [[date1,date2,date3], [date4,date5,date6,date7]]}
        suspension_dks: список дат DK из periods_suspension
        period_type: "pmp" или "gss"
    
    Returns:
        словарь вида {"0": [{"DN": date, "DK": date, "amount": float}, ...]}
    """
    # Выбираем нужный словарь стандартов
    standart_dict = PMP_STANDART if period_type == "pmp" else GSS_STANDART
   
    SP_STANDART = await pension_insurance_SPK_amount(data)
    
    result = {}
    
    for pension_id, period_lists in periods_data.items():
        pension_periods = []
        prev_amount = None
        
        for date_list in period_lists:
            # Разрезаем на пары и сразу считаем amount
            for i in range(len(date_list) - 1):
                start = date_list[i]
                end = date_list[i + 1]
                
                amount = calculate_amount_for_period(
                    start_date=start,
                    end_date=end,
                    suspension_dks=suspension_dks,
                    standart_dict=standart_dict,
                    prev_amount=prev_amount,
                    pension_id=pension_id,
                    SP_STANDART=SP_STANDART
                )
                
                pension_periods.append({
                    "DN": start,
                    "DK": end,
                    "amount": amount
                })
                
                prev_amount = amount
        
        result[pension_id] = pension_periods
    
    return result

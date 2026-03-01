from src.schemas.json_query_schema import (
    PaymentInterface,
)
from datetime import date
from typing import List, Optional


async def get_date_init_pension_Moscow(payments: List[PaymentInterface]) -> Optional[date]:
    """
    Возвращает дату назначения первой пенсии в Москве
    
    Returns:
        Optional[date]: Дата назначения первой пенсии в Москве или None, если такой пенсии нет
    """
    
    for payment in payments:
        if payment.is_Moscow and payment.type == "pension":
            return payment.DN
    return None


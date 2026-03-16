from src.schemas.json_query_schema import (
    PaymentInterface,
)
from datetime import date
from typing import List, Optional


async def get_first_moscow_pension(payments: List[PaymentInterface]) -> Optional[PaymentInterface]:
    """
    Возвращает объект - первую пенсию, назначенную в Москве
    
    Returns:
        Optional[PaymentInterface]: Первая пенсия, назначенная в Москве
    """
    
    for payment in payments:
        if payment.is_Moscow and payment.type == "pension":
            return payment
        elif payment.type in ["edv", "egdv", "housing", "edk"]:
            return payment
    return None

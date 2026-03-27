from src.schemas.json_query_schema import JsonQuerySchema
from dateutil.relativedelta import relativedelta

def sort_periods_in_data(data: JsonQuerySchema) -> JsonQuerySchema:
    """
    Сортирует периоды регистрации в Москве по дате начала (DN) внутри структуры data.
    Сортирует поля: periods_reg_moscow, periods_reg_representative_moscow, periods_reg_breadwinner_moscow,  periods_suspension, periods_inpatient, payments
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
        
    # Сортируем периоды приостановок выплат
    if data.periods_suspension:
        data.periods_suspension = sorted(
            data.periods_suspension, 
            key=lambda period: period.DN
        )
        
    # Сортируем периоды стационаризации
    if data.periods_inpatient:
        data.periods_inpatient = sorted(
            data.periods_inpatient, 
            key=lambda period: period.DN
        )

    # Сортируем периоды выплат
    if data.payments:
        data.payments = sorted(
            data.payments,
            key=lambda payment: payment.DN
        )
    
    return data


async def is_adult(today, date_of_birth, is_adult: bool) -> tuple[bool, str | None]:
    """
    Проверяет, является ли человек совершеннолетним (достиг 18 лет)
    
    Returns:
        tuple[bool, str | None]: (соответствие ожидаемому статусу, сообщение об ошибке)
    """
    delta = relativedelta(today, date_of_birth)
    is_adult_result = delta.years >= 18
    
    if is_adult_result == True and is_adult == True:
        return True, None

    elif is_adult_result == False and is_adult == False:
        return False, None
    
    return False, "Фактический возраст расходится с выбранной категорией гражданина (взрослый, ребенок)"




from src.schemas.json_query_schema import JsonQuerySchema


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





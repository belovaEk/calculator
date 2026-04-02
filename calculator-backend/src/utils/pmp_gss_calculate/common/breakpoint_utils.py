from src.schemas.json_query_schema import JsonQuerySchema
from datetime import timedelta
from src.utils.payments.types.paymentType import PeriodAmount

async def get_breakpoints_date(data: JsonQuerySchema):
    '''
    Функция возвращает массив breakpoints, построенный по принципу:
    1. Добавляет дату начала первой пенсии;
    2. Функця смотрит типы всех московских пенсий, и если они меняются, то добавляет дату в breakpoints;
    3. Добавляет дату конца последней пенсии.

    Пример массива breakpoints:
    [Дата начала первой пенсии; Дата изменения пенсии i-ая; Дата изменения пенсии i+1-ая; ... ; Дата конца последней пенсии]
    '''

    # Получаем список московских пенсий
    pensions = [p for p in data.payments if p.type == 'pension' and p.is_Moscow == True]

    # На всякий случай сортируем пенсии
    pensions = sorted(pensions, key=lambda p: p.DN)

    # Инициализируем целевой массив
    breakpoints = []

    if pensions:
        # Добавляем дату начала первой пенсии в breakpoints
        breakpoints.append(pensions[0].DN)
        for i in range(len(pensions)-1):
            if pensions[i].categoria != pensions[i+1].categoria:
                # Добавляем дату смена вида пенсии
                breakpoints.append(pensions[i+1].DN)
                
        # Добавляем дату конца последней пенсии в breakpoints
        breakpoints.append(pensions[-1].DK)

        # Оставляем только уникальные значения
        breakpoints_unique_list = sorted(set(breakpoints))

        return breakpoints_unique_list

    else: 
        # Если московских пенсий нет, возвращаем пустой массив
        return []



def split_pmp_periods_by_breakpoints(pmp_or_gss_periods: dict, breakpoints: list):
    """
    Разбивает периоды в pmp_periods по точкам из breakpoints
    """
    periods = pmp_or_gss_periods[0]
    sorted_breakpoints = sorted(set(breakpoints))
    
    new_periods = []
    
    for period in periods:
        current_start = period.DN
        current_end = period.DK
        current_amount = period.amount
        
        # Находим все breakpoints, которые попадают внутрь текущего периода (исключая границы)
        breakpoints_in_period = [
            bp for bp in sorted_breakpoints 
            if current_start < bp <= current_end
        ]
        
        if not breakpoints_in_period:
            # Если нет точек разбиения внутри периода, оставляем как есть
            new_periods.append(period)
        else:
            # Разбиваем период по точкам
            segment_start = current_start
            
            for bp in breakpoints_in_period:
                # Первый сегмент: от segment_start до bp - 1 день
                if segment_start <= bp - timedelta(days=1):
                    new_periods.append(
                        PeriodAmount(
                            DN=segment_start,
                            DK=bp - timedelta(days=1),
                            amount=current_amount
                        )
                    )
                # Второй сегмент: от bp до текущего конца (будет продолжен в следующей итерации)
                segment_start = bp
            
            # Последний сегмент: от последнего breakpoint до current_end
            if segment_start <= current_end:
                new_periods.append(
                    PeriodAmount(
                        DN=segment_start,
                        DK=current_end,
                        amount=current_amount
                    )
                )
    
    # Обновляем pmp_periods
    pmp_or_gss_periods[0] = new_periods
    
    return pmp_or_gss_periods
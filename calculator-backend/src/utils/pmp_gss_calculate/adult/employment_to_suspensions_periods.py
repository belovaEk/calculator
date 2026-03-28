from src.schemas.json_query_schema import (
    PeriodType,
    PeriodWithIdType,
)
from typing import List
from datetime import date
from dateutil.relativedelta import relativedelta


async def employment_to_suspensions_periods(
    employment_periods: List[PeriodType], 
    suspension_periods: List[PeriodType]
) -> List[PeriodType]:
    """
    Преобразует периоды трудоустройства в периоды приостановок выплат
    Цель - сверить и дозаписать пропущенные периоды трудоустройства в периоды приостановок
    """
    
    # Создаём копию suspension_periods для модификации
    result = suspension_periods.copy()
    
    i = 0
    while i < len(result):
        modified = False
        for emp in employment_periods:
            # Проверяем пересечение периодов
            if result[i].DN < emp.DK and emp.DN < result[i].DK:
                # Здесь ваша логика обработки пересечений
                if emp.DN <= result[i].DN and result[i].DK <= emp.DK:
                    # Период приостановки внутри трудоустройства
                    # Можно заменить на уточнённые даты
                    result[i] = PeriodType(
                        id=result[i].id,
                        DN=max(result[i].DN, emp.DN),
                        DK=min(result[i].DK, emp.DK)
                    )
                    modified = True
                    break
                elif result[i].DN < emp.DN <= result[i].DK:
                    result[i] = PeriodType(
                        id=result[i].id,
                        DN=result[i].DN,
                        DK=emp.DK
                    )
                    modified = True
                    break
                elif emp.DN <= result[i].DN < emp.DK:
                    result[i] = PeriodType(
                        id=result[i].id,
                        DN=emp.DN,
                        DK=result[i].DK
                    )
                    modified = True
                    break
        
        if modified:
            i += 1
        else:
            i += 1
    
    return result
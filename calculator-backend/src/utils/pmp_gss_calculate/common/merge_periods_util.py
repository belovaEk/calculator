from typing import List
from src.schemas.json_query_schema import PeriodType

async def merge_periods(periods: List[PeriodType]) -> List[PeriodType]:

    periods.sort(key=lambda x: x.DN)

    new_periods = []
    i = 0   

    while i < len(periods):
        current = periods[i]
        
        # Проверяем следующие периоды на возможность объединения
        j = i + 1
        while j < len(periods):
            next_period = periods[j]
            
            # Если текущий период заканчивается там, где начинается следующий
            if current.DK >= next_period.DN:
                # Объединяем периоды
                current = PeriodType(DN=current.DN, DK=next_period.DK)
                j += 1
            else:
                break
        
        new_periods.append(current)
        i = j

    print(new_periods)

    return new_periods
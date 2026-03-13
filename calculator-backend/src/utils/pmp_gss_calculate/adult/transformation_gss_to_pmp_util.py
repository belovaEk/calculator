from typing import List
from src.schemas.json_query_schema import PeriodType

async def transformation_gss_to_pmp(gss_periods: List[PeriodType], pmp_periods: List[PeriodType]):
    new_pmp_periods: List[PeriodType] = gss_periods + pmp_periods
    new_pmp_periods.sort(key=lambda x: x.DN)
    print(new_pmp_periods)

    merged_periods = []
    i = 0   
    print(45)

    while i < len(new_pmp_periods):
        current = new_pmp_periods[i]
        
        # Проверяем следующие периоды на возможность объединения
        j = i + 1
        while j < len(new_pmp_periods):
            next_period = new_pmp_periods[j]
            
            # Если текущий период заканчивается там, где начинается следующий
            if current.DK == next_period.DN:
                # Объединяем периоды
                current = PeriodType(DN=current.DN, DK=next_period.DK)
                j += 1
            else:
                break
        
        merged_periods.append(current)
        i = j

    print(merged_periods)

    return {
        "pmp_periods": merged_periods,
        "gss_periods": []
    }

from src.schemas.json_query_schema import (
    PeriodType,
    PeriodWithIdType,
)
from typing import List


async def employment_to_suspensions_periods(employment_periods: List[PeriodType], suspension_periods: List[PeriodType]) -> List[PeriodType]:
    """
    Преобразует периоды трудоустройства в периоды приостановок выплат
    Цель - сверить и дозаписать пропущенные периоды трудоустройства в периоды приостановок
    """
    #{suspence_res:[{id=0, DN=01.06.2022, DK=01.07.2022}, {id=1, DN=01.06.2023, DK=04.12.2023}}]

    for i in range(len(suspension_periods)):
        for j in range(len(employment_periods)):
            if employment_periods[j].DN <= suspension_periods[i].DN < employment_periods[j].DK <= suspension_periods[i].DK:
                #Удаляем период Дата приостановки i; Дата возобновления i из периодов приостановок
                suspension_periods.pop(i)
                #На место периода i  в периоды приостановок записываем период Дата трудоустройства j; Дата возобновления i
                suspension_periods.insert(i, PeriodType(id=suspension_periods[i].id, DN=employment_periods[j].DN, DK=suspension_periods[i].DK))
                continue
            elif suspension_periods[i].DN < employment_periods[j].DN < suspension_periods[i].DK < employment_periods[j].DK:
                suspension_periods.pop(i)
                #На место периода i в периоды приостановок записываем период Дата приостановки i; Дата увольнения j
                suspension_periods.insert(i, PeriodType(id=suspension_periods[i].id, DN=suspension_periods[i].DN, DK=employment_periods[j].DK))
                continue
            elif employment_periods[j].DN < suspension_periods[i].DN < suspension_periods[i].DK < employment_periods[j].DK:
                suspension_periods.pop(i)
                #Добавляем в периоды приостановок период Дата трудоустройства j; Дата увольнения j
                suspension_periods.insert(i, PeriodType(id=suspension_periods[i].id, DN=employment_periods[j].DN, DK=employment_periods[j].DK))
                continue
    return suspension_periods
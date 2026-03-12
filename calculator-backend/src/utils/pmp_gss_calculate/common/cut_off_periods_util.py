from datetime import date
from typing import List

from src.schemas.json_query_schema import PeriodType, PeriodWithIdType


async def cut_off_periods_before_change_date(
    periods: List[PeriodWithIdType],
    change_last_date: date,
) -> List[PeriodWithIdType]:
    """
    Отсекает все периоды стационаризации, которые полностью
    находятся до даты последнего изменения данных в выплате,
    и обрезает периоды, начавшиеся до этой даты.

    Цель соответствует схеме: оставить только ту часть периода
    нахождения в стационарном учреждении, которая идет после
    даты последнего изменения данных в выплате.
    """
    if not periods:
        return []

    new_periods_inpatient: List[PeriodWithIdType] = []
    
    for period in periods:

        DN = period.DN
        DK = period.DK

        if change_last_date <= DN < DK:
            new_periods_inpatient.append(PeriodWithIdType(id=period.id, DN=DN, DK=DK))
        elif DN <= change_last_date < DK:
            new_periods_inpatient.append(PeriodWithIdType(id=period.id, DN=change_last_date, DK=DK))


        # # Если стационар закончился до или в дату изменения выплаты — пропускаем
        # if period.DK <= change_last_date:
        #     continue

        # # Новая дата начала — максимум из DN и даты изменения выплаты
        # new_dn = max(period.DN, change_last_date)
        # new_dk = period.DK

        # # Защита от вырожденных периодов
        # if new_dn < new_dk:
        #     result.append(PeriodType(DN=new_dn, DK=new_dk))

    return new_periods_inpatient

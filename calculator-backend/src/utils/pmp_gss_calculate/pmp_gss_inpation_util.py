from datetime import date
from typing import List

from src.schemas.json_query_schema import PeriodType


async def filter_inpatient_periods_after_change_date(
    periods_inpatient: List[PeriodType],
    change_last_date: date,
) -> List[PeriodType]:
    """
    Отсекает все периоды стационаризации, которые полностью
    находятся до даты последнего изменения данных в выплате,
    и обрезает периоды, начавшиеся до этой даты.

    Цель соответствует схеме: оставить только ту часть периода
    нахождения в стационарном учреждении, которая идет после
    даты последнего изменения данных в выплате.
    """
    if not periods_inpatient:
        return []

    result: List[PeriodType] = []

    for period in periods_inpatient:
        # Если стационар закончился до или в дату изменения выплаты — пропускаем
        if period.DK <= change_last_date:
            continue

        # Новая дата начала — максимум из DN и даты изменения выплаты
        new_dn = max(period.DN, change_last_date)
        new_dk = period.DK

        # Защита от вырожденных периодов
        if new_dn < new_dk:
            result.append(PeriodType(DN=new_dn, DK=new_dk))

    return result

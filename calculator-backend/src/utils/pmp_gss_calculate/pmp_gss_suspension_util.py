from src.schemas.json_query_schema import JsonQuerySchema, PeriodType, PeriodWithIdType
from typing import List


async def pmp_gss_suspension(
    data: JsonQuerySchema, pmp_periods: List[PeriodType], gss_periods: List[PeriodType]
):
    """Функция для пересчета ГСС и ПМП с учетом периодов прерываний

    Args:
        data (JsonQuerySchema):
        pmp_periods (List[PeriodType]): периоды ПМП с учетом регистрации
        gss_periods (List[PeriodType]): периоды ГСС с учетом регистрации

    Returns:
        dict: Словарь с ключами
        - PMP: List[PeriodType] - ПМП с учетом прерываний
        - GSS: List[PeriodType] - ГСС с учетом прерываний
    """
    periods_suspension = data.periods_suspension or None

    if periods_suspension:
        gss_periods = await recalculation(gss_periods, periods_suspension)
        pmp_periods = await recalculation(pmp_periods, periods_suspension)

    return {"PMP": pmp_periods, "GSS": gss_periods}


async def recalculation(
    periods: List[PeriodType], periods_suspension: List[PeriodWithIdType]
):
    """Вспомогательная функция для пересчета ГСС и ПМП с учетом периодов прерываний

    Args:
        periods (List[PeriodType]): периоды ПМП или ГСС с учетом регистрации
        periods_suspension (List[PeriodWithIdType]): периоды прерывания

    Returns:
        List[PeriodType]: новый массив ПМП или ГСС с учето прерываний
    """

    current_gss_pmp: List[PeriodType] = periods.copy()

    for suspension in periods_suspension:

        new_periods: List[PeriodType] = []

        DNsus = suspension.DN  # дата приостановки
        DKsus = suspension.DK  # дата возобновления

        for period in current_gss_pmp:

            DN_gss_pmp = period.DN  # дата начала ГСС или ПМП
            DK_gss_pmp = period.DK  # дата конца ГСС или ПМП

            # Если дата приостановки пенсии попала между датами выплаты ГСС или ПМП
            if DN_gss_pmp < DNsus < DK_gss_pmp < DKsus:
                new_periods.append(PeriodType(DN=DN_gss_pmp, DK=DNsus))

            # Еcли между датами периода выплат ГСС или ПМП попадает дата возобновления выплаты пенсии
            elif DNsus < DN_gss_pmp < DKsus < DK_gss_pmp:
                new_periods.append(PeriodType(DN=DKsus, DK=DK_gss_pmp))

            # Если период выплаты ГСС или ПМП у нас попадает между двумя датами приостановки и возобновления пенсии
            elif DNsus < DN_gss_pmp < DK_gss_pmp < DKsus:
                continue

            # Если даты приостановки и возобновления наоборот попадают внутрь периода выплат ГСС или ПМП
            elif DN_gss_pmp < DNsus < DKsus < DK_gss_pmp:
                new_periods.append(PeriodType(DN=DN_gss_pmp, DK=DNsus))
                new_periods.append(PeriodType(DN=DKsus, DK=DK_gss_pmp))

            # Если не подпал под условия добавляем исходный период
            else:
                new_periods.append(period)

        current_gss_pmp = new_periods

    return current_gss_pmp

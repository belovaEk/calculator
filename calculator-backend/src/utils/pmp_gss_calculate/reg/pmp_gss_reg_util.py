from src.schemas.json_query_schema import PeriodType
from datetime import date
from typing import List


async def pmp_gss_registration(
    dr10: date,
    spv_init_date: date,
    list_of_periods_reg: List[PeriodType],
    pmp_periods: List[PeriodType],
    gss_periods: List[PeriodType],
) -> dict:
    """
    Возвращает ПМП и ГСС в зависимости от ДР10 и ДатыПервойСПВ

    Returns:
        dict: Словарь с ключами:
            - pmp_periods: List[PeriodType] - периоды, когда был назначен прожиточный минимум пенсионера (ПМП)
            - gss_periods: List[PeriodType] - периоды, когда был назначен городской социальный стандарт (ГСС)

    {pmp_periods: [{'DN':DNreg, 'DK': DKreg}, {'DN':DNreg, 'DK': DKreg}],
    gss_periods: [{'DN':DNreg, 'DK': DKreg}, {'DN':DNreg, 'DK': DKreg}]}
    """

    if dr10 < spv_init_date:
        return await dr10_earlier(
            spv_init_date, list_of_periods_reg, pmp_periods, gss_periods
        )
    else:
        return await spv_init_date_earlier(
            dr10, spv_init_date, list_of_periods_reg, pmp_periods, gss_periods
        )


async def spv_init_date_earlier(
    dr10: date,
    spv_init_date: date,
    list_of_periods_reg: List[PeriodType],
    pmp_periods: List[PeriodType],
    gss_periods: List[PeriodType],
) -> dict:
    """
    Обрабатывает случай, когда дата первой СПВ раньше даты достижения 10 лет регистрации

    Returns:
        dict: Словарь с ключами:
            - pmp_periods: List[PeriodType] - периоды, когда был назначен прожиточный минимум пенсионера (ПМП)
            - gss_periods: List[PeriodType] - периоды, когда был назначен городской социальный стандарт (ГСС)
    """
    i = 0
    n = len(list_of_periods_reg)

    currentDate = date.today()

    pmp_periods.append(PeriodType(DN=spv_init_date, DK=dr10))

    while i <= n - 1:

        DKreg = list_of_periods_reg[i].DK
        DNreg = list_of_periods_reg[i].DN

        if DKreg >= dr10 >= DNreg:
            if i == n - 1:
                gss_periods.append(PeriodType(DN=dr10, DK=DKreg))
                if DKreg != currentDate:
                    pmp_periods.append(PeriodType(DN=DKreg, DK=currentDate))
            else:
                gss_periods.append(PeriodType(DN=dr10, DK=DKreg))
                pmp_periods.append(
                    PeriodType(DN=DKreg, DK=list_of_periods_reg[i + 1].DN)
                )

        elif DNreg > dr10 and DKreg > dr10:
            if i == n - 1:
                gss_periods.append(PeriodType(DN=DNreg, DK=DKreg))
                if DKreg != currentDate:
                    pmp_periods.append(PeriodType(DN=DKreg, DK=currentDate))
            else:
                gss_periods.append(PeriodType(DN=DNreg, DK=DKreg))
                pmp_periods.append(
                    PeriodType(DN=DKreg, DK=list_of_periods_reg[i + 1].DN)
                )
        i += 1

    return {"pmp_periods": pmp_periods, "gss_periods": gss_periods}


async def dr10_earlier(
    spv_init_date: date,
    list_of_periods_reg: List[PeriodType],
    pmp_periods: List[PeriodType],
    gss_periods: List[PeriodType],
) -> dict:
    """
    Обрабатывает случай, когда дата достижения 10 лет регистрации раньше даты первой СПВ

    Returns:
        dict: Словарь с ключами:
            - pmp_periods: List[PeriodType] - периоды, когда был назначен прожиточный минимум пенсионера (ПМП)
            - gss_periods: List[PeriodType] - периоды, когда был назначен городской социальный стандарт (ГСС)

    """
    i = 0
    n = len(list_of_periods_reg)
    currentDate = date.today()

    while i <= n - 1:
        DKreg = list_of_periods_reg[i].DK
        DNreg = list_of_periods_reg[i].DN

        # Если дата попадает на период регистрации

        if DKreg > spv_init_date >= DNreg:
            if i == n - 1:
                gss_periods.append(PeriodType(DN=spv_init_date, DK=DKreg))
                if DKreg != currentDate:
                    pmp_periods.append(PeriodType(DN=DKreg, DK=currentDate))
            else:
                gss_periods.append(PeriodType(DN=spv_init_date, DK=DKreg))
                pmp_periods.append(
                    PeriodType(DN=DKreg, DK=list_of_periods_reg[i + 1].DN)
                )

        # Если период регистрации больше даты назначения первой пенсии
        elif spv_init_date < DNreg < DKreg:

            if i == n - 1:
                gss_periods.append(PeriodType(DN=DNreg, DK=DKreg))
                if DKreg != currentDate:
                    pmp_periods.append(PeriodType(DN=DKreg, DK=currentDate))
            else:
                gss_periods.append(PeriodType(DN=DNreg, DK=DKreg))
                pmp_periods.append(
                    PeriodType(DN=DKreg, DK=list_of_periods_reg[i + 1].DN)
                )

        elif i == n - 1:
            if DKreg <= spv_init_date:
                pmp_periods.append(PeriodType(DN=spv_init_date, DK=currentDate))

        # Если дата назначения первой пенсии попала между периодами регистрации
        elif DKreg <= spv_init_date < list_of_periods_reg[i + 1].DN:
            pmp_periods.append(PeriodType(DN=spv_init_date, DK=DNreg))
        i += 1

    return {"pmp_periods": pmp_periods, "gss_periods": gss_periods}

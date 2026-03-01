from datetime import date
from typing import List
from src.schemas.json_query_schema import PeriodType


def merge_periods(periods: List[PeriodType]) -> List[PeriodType]:
    """
    Объединяет пересекающиеся и соприкасающиеся периоды.

    Функция сортирует периоды по дате начала и последовательно объединяет их,
    если текущий период пересекается или соприкасается со следующим.

    Args:
        periods: Список периодов для объединения

    Returns:
        List[PeriodType]: Новый список с объединенными периодами
    """
    if not periods:
        return []

    # Сортируем периоды по дате начала
    sorted_periods = sorted(periods, key=lambda x: x.DN)

    merged = []
    current = sorted_periods[0]

    for next_period in sorted_periods[1:]:
        # Проверяем пересечение или соприкосновение
        if current.DK >= next_period.DN:
            # Объединяем: берем максимальную дату окончания
            current = PeriodType(DN=current.DN, DK=max(current.DK, next_period.DK))
        else:
            # Нет пересечения - добавляем текущий и переходим к следующему
            merged.append(current)
            current = next_period

    # Добавляем последний период
    merged.append(current)

    return merged


async def pmp_gss_inpatient(
    pmp_periods: List[PeriodType],
    gss_periods: List[PeriodType],
    periods_inpatient: List[PeriodType],
) -> dict:
    """
    Обрабатывает пересечения периодов ГСС с периодами нахождения в стационаре.

    При нахождении человека в стационаре выплата ГСС заменяется на выплату ПМП.
    Функция находит все пересечения и корректно перераспределяет периоды.

    Args:
        pmp_periods: Исходные периоды выплаты ПМП
        gss_periods: Исходные периоды выплаты ГСС
        periods_inpatient: Периоды нахождения в стационаре

    Returns:
        dict: Словарь с обновленными периодами:
            - pmp_periods: List[PeriodType] - обновленные периоды ПМП
            - gss_periods: List[PeriodType] - обновленные периоды ГСС
    """

    # Создаем копии списков
    result_pmp = list(pmp_periods) if pmp_periods else []
    result_gss = list(gss_periods) if gss_periods else []

    # Сортируем все входные периоды по дате начала
    result_pmp.sort(key=lambda x: x.DN)
    result_gss.sort(key=lambda x: x.DN)
    sorted_inpatient = (
        sorted(periods_inpatient, key=lambda x: x.DN) if periods_inpatient else []
    )

    for inpatient in sorted_inpatient:
        new_gss = []
        inpatient_start = inpatient.DN
        inpatient_end = inpatient.DK

        for gss in result_gss:
            gss_start = gss.DN
            gss_end = gss.DK

            # Проверяем наличие пересечения
            if gss_end < inpatient_start or gss_start > inpatient_end:
                new_gss.append(gss)
                continue

            # Случай 3: ГСС полностью внутри стационара
            if gss_start >= inpatient_start and gss_end <= inpatient_end:
                result_pmp.append(PeriodType(DN=gss_start, DK=gss_end))
                continue

            # Случай 4: Стационар полностью внутри ГСС
            if inpatient_start > gss_start and inpatient_end < gss_end:
                new_gss.append(PeriodType(DN=gss_start, DK=inpatient_start))
                result_pmp.append(PeriodType(DN=inpatient_start, DK=inpatient_end))
                new_gss.append(PeriodType(DN=inpatient_end, DK=gss_end))
                continue

            # Случай 1: Стационар начался внутри ГСС и закончился после ГСС
            if gss_start <= inpatient_start <= gss_end and inpatient_end > gss_end:
                if gss_start < inpatient_start:
                    new_gss.append(PeriodType(DN=gss_start, DK=inpatient_start))
                result_pmp.append(PeriodType(DN=inpatient_start, DK=gss_end))
                continue

            # Случай 2: Стационар начался до ГСС и закончился внутри ГСС
            if inpatient_start < gss_start <= inpatient_end <= gss_end:
                result_pmp.append(PeriodType(DN=gss_start, DK=inpatient_end))
                if inpatient_end < gss_end:
                    new_gss.append(PeriodType(DN=inpatient_end, DK=gss_end))
                continue

            # На всякий случай, если ни одно условие не подошло
            new_gss.append(gss)

        result_gss = new_gss

    # Сортируем финальные списки
    result_pmp.sort(key=lambda x: x.DN)
    result_gss.sort(key=lambda x: x.DN)

    return {"pmp_periods": result_pmp, "gss_periods": result_gss}

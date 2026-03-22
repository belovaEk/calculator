from datetime import date, timedelta
from typing import List
from src.schemas.json_query_schema import PeriodType
from dateutil.relativedelta import relativedelta



# def merge_periods(periods: List[PeriodType]) -> List[PeriodType]:
#     """
#     Объединяет пересекающиеся и соприкасающиеся периоды.

#     Функция сортирует периоды по дате начала и последовательно объединяет их,
#     если текущий период пересекается или соприкасается со следующим.

#     Args:
#         periods: Список периодов для объединения

#     Returns:
#         List[PeriodType]: Новый список с объединенными периодами
#     """
#     if not periods:
#         return []

#     # Сортируем периоды по дате начала
#     sorted_periods = sorted(periods, key=lambda x: x.DN)

#     merged = []
#     current = sorted_periods[0]

#     for next_period in sorted_periods[1:]:
#         # Проверяем пересечение или соприкосновение
#         if current.DK >= next_period.DN:
#             # Объединяем: берем максимальную дату окончания
#             current = PeriodType(DN=current.DN, DK=max(current.DK, next_period.DK))
#         else:
#             # Нет пересечения - добавляем текущий и переходим к следующему
#             merged.append(current)
#             current = next_period

#     # Добавляем последний период
#     merged.append(current)

#     return merged


async def pmp_gss_inpatient(
    pmp_periods: List[PeriodType],
    gss_periods: List[PeriodType],
    periods_inpatient: List[PeriodType],
) -> dict:
    """
    Обрабатывает пересечения периодов ГСС с периодами нахождения в стационаре.
    При нахождении человека в стационаре выплата ГСС заменяется на выплату ПМП.
    Стационар влияет на выплаты с 1-го числа месяца, следующего за месяцем начала стационара.
    Функция находит все пересечения и корректно перераспределяет периоды.

    Args:
        pmp_periods: Исходные периоды выплаты ПМП
        gss_periods: Исходные периоды выплаты ГСС
        periods_inpatient: Периоды нахождения в стационаре

    Returns:
        dict: Словарь с обновленными периодами:
            - pmp_periods: GssPmpPensionType - обновленные периоды ПМП
            - gss_periods: GssPmpPensionType - обновленные периоды ГСС
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

    def get_effect_start_date(inpatient_start: date) -> date:
        """Возвращает дату начала влияния стационара (1-е число следующего месяца)"""
        # Переход на первое число следующего месяца
        return (inpatient_start.replace(day=1) + relativedelta(months=1))

    def merge_periods(periods: List[PeriodType]) -> List[PeriodType]:
        """Объединяет пересекающиеся и смежные периоды"""
        if not periods:
            return []
        
        merged = []
        sorted_periods = sorted(periods, key=lambda x: x.DN)
        current = sorted_periods[0]
        
        for next_period in sorted_periods[1:]:
            # Если периоды пересекаются или соприкасаются
            if next_period.DN <= current.DK:
                current = PeriodType(
                    DN=current.DN,
                    DK=max(current.DK, next_period.DK)
                )
            else:
                merged.append(current)
                current = next_period
        
        merged.append(current)
        return merged

    for inpatient in sorted_inpatient:
        new_gss = []

        # Дата начала влияния стационара (1-е число следующего месяца)
        effect_start = get_effect_start_date(inpatient.DN)
        effect_end = inpatient.DK
        
        # Если эффект начинается после окончания стационара, пропускаем
        if effect_start > effect_end:
            # Стационар не влияет на выплаты, добавляем все ГСС как есть
            new_gss = result_gss
            result_gss = new_gss
            continue
        

        for gss in result_gss:
            gss_start = gss.DN
            gss_end = gss.DK

            # Проверяем наличие пересечения с периодом влияния стационара
            if gss_end < effect_start or gss_start > effect_end:
                # Нет пересечения - оставляем ГСС как есть
                new_gss.append(gss)
                continue

            # Случай 1: ГСС полностью внутри периода влияния стационара
            if gss_start >= effect_start and gss_end <= effect_end:
                # Весь период ГСС заменяется на ПМП
                result_pmp.append(PeriodType(DN=gss_start, DK=gss_end))
                continue

            # Случай 2: Период влияния стационара полностью внутри ГСС
            if effect_start >= gss_start and effect_end <= gss_end:
                # Часть ГСС до стационара
                if effect_start > gss_start:
                    new_gss.append(PeriodType(DN=gss_start, DK=effect_start-timedelta(days=1)))
                # Часть ГСС после стационара
                if effect_end < gss_end:
                    new_gss.append(PeriodType(DN=effect_end+timedelta(days=1), DK=gss_end))
                # Период стационара в ПМП
                result_pmp.append(PeriodType(DN=effect_start, DK=effect_end))
                continue

            # Случай 3: Стационар начался внутри ГСС и закончился после ГСС
            if gss_start <= effect_start <= gss_end and effect_end > gss_end:
                # Часть ГСС до стационара
                if gss_start < effect_start:
                    new_gss.append(PeriodType(DN=gss_start, DK=effect_start-timedelta(days=1)))
                # Часть ГСС до конца периода (весь остаток в ПМП)
                result_pmp.append(PeriodType(DN=effect_start, DK=gss_end))
                continue

            # Случай 4: Стационар начался до ГСС и закончился внутри ГСС
            if effect_start < gss_start <= effect_end <= gss_end:
                # Часть ГСС с начала влияния до конца ГСС (весь период в ПМП)
                result_pmp.append(PeriodType(DN=gss_start, DK=effect_end))
                # Часть ГСС после стационара
                if effect_end < gss_end:
                    new_gss.append(PeriodType(DN=effect_end+timedelta(days=1), DK=gss_end))
                continue

        result_gss = new_gss

    # Объединяем пересекающиеся периоды в ПМП и ГСС
    result_pmp = merge_periods(result_pmp)
    result_gss = merge_periods(result_gss)

    # Сортируем финальные списки
    result_pmp.sort(key=lambda x: x.DN)
    result_gss.sort(key=lambda x: x.DN)

    return {"pmp_periods": {0: result_pmp}, "gss_periods": {0: result_gss}}

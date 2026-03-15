import datetime
from typing import Dict, Any

PeriodDict = Dict[int, Dict[str, Any]]


def _get_pension_dates(periods: PeriodDict):
    sorted_keys = sorted(periods.keys())
    date_start = periods[sorted_keys[0]]['date_start']
    date_end = periods[sorted_keys[-1]]['date_end']
    print(f"_get_pension_dates: earliest start = {date_start}, latest end = {date_end}")
    return date_start, date_end


def _build_result_peresech(
    itog_periods: PeriodDict,
    pension_l_periods: PeriodDict,
    date_start_inter: datetime.date,
    date_end_inter: datetime.date,
) -> PeriodDict:
    """
    Строит результирующие подпериоды внутри зоны пересечения двух пенсий.

    Исправленная версия: использует sweep line внутри зоны — собирает все
    граничные даты из k- и j-периодов, делит зону на атомарные подотрезки
    и для каждого считает сумму.

    Ключевое исправление бага: k-only подотрезки (где pension_l имеет разрыв)
    ранее отфильтровывались по summa_3 == 0. Теперь они сохраняются с
    summa_3 = summa_1, так как itog должен выплачиваться и в эти периоды.

    Отфильтровываются только подотрезки, где активен исключительно pension_l
    (summa_1 == 0) — они обрабатываются через _periods_before/_periods_after.
    """
    print(f"\n_build_result_peresech: interval = {date_start_inter} — {date_end_inter}")

    # Клиппингуем k-периоды к зоне
    k_segs = []
    for pk in itog_periods.values():
        ds = max(pk['date_start'], date_start_inter)
        de = min(pk['date_end'], date_end_inter)
        if ds < de:
            k_segs.append((ds, de, pk['summa']))
            print(f" itog seg в зоне: {ds} — {de}, summa={pk['summa']}")

    # Клиппингуем j-периоды к зоне
    j_segs = []
    for pj in pension_l_periods.values():
        ds = max(pj['date_start'], date_start_inter)
        de = min(pj['date_end'], date_end_inter)
        if ds < de:
            j_segs.append((ds, de, pj['summa']))
            print(f" pension_l seg в зоне: {ds} — {de}, summa={pj['summa']}")

    # Sweep line: все граничные даты внутри зоны
    breakpoints = sorted({
        d
        for seg_list in (k_segs, j_segs)
        for (a, b, _) in seg_list
        for d in (a, b)
    } | {date_start_inter, date_end_inter})

    raw = []
    for i in range(len(breakpoints) - 1):
        ds = breakpoints[i]
        de = breakpoints[i + 1]
        sum_k = sum(s for a, b, s in k_segs if a <= ds < b)
        sum_j = sum(s for a, b, s in j_segs if a <= ds < b)
        summ = sum_k + sum_j
        print(f"  подотрезок {ds} — {de}: sum_k={sum_k}, sum_j={sum_j}, summ={summ}")
        if summ > 0:
            raw.append({
                'date_start': ds, 'date_end': de,
                'summa_1': sum_k, 'summa_2': sum_j, 'summa_3': summ,
            })

    # Отфильтровываем только pension_l-only записи (sum_k == 0):
    # они обрабатываются снаружи через _periods_before/_periods_after.
    filtered = [e for e in raw if e['summa_1'] > 0]
    filtered.sort(key=lambda e: e['date_start'])

    print(f"_build_result_peresech: результат {len(filtered)} записей")
    for f in filtered:
        print(" ", f)

    return {idx: entry for idx, entry in enumerate(filtered)}


def _periods_before(periods: PeriodDict, cutoff: datetime.date) -> list[dict]:
    print(f"_periods_before: cutoff = {cutoff}")
    result = []
    for idx in sorted(periods.keys()):
        p = periods[idx]
        print(f" checking period {idx}: {p['date_start']} — {p['date_end']}, summa={p['summa']}")
        if p['date_start'] >= cutoff:
            print("  -> период начинается после cutoff, прерываем")
            break
        if p['date_end'] <= cutoff:
            entry = {'date_start': p['date_start'], 'date_end': p['date_end'], 'summa': p['summa']}
            result.append(entry)
            print(f"  -> полностью до cutoff, добавить: {entry}")
        else:
            entry = {'date_start': p['date_start'], 'date_end': cutoff, 'summa': p['summa']}
            result.append(entry)
            print(f"  -> частично до cutoff, добавить усеченный: {entry}")
    print(f"_periods_before: returning {len(result)} entries")
    return result


def _periods_after(periods: PeriodDict, cutoff: datetime.date) -> list[dict]:
    print(f"_periods_after: cutoff = {cutoff}")
    result = []
    for idx in sorted(periods.keys()):
        p = periods[idx]
        print(f" checking period {idx}: {p['date_start']} — {p['date_end']}, summa={p['summa']}")
        if p['date_end'] <= cutoff:
            print("  -> период заканчивается до или в cutoff, пропускаем")
            continue
        if p['date_start'] >= cutoff:
            entry = {'date_start': p['date_start'], 'date_end': p['date_end'], 'summa': p['summa']}
            result.append(entry)
            print(f"  -> полностью после cutoff, добавить: {entry}")
        else:
            entry = {'date_start': cutoff, 'date_end': p['date_end'], 'summa': p['summa']}
            result.append(entry)
            print(f"  -> частично после cutoff, добавить усеченный: {entry}")
    print(f"_periods_after: returning {len(result)} entries")
    return result


def _merge_two_pensions(
    itog_periods: PeriodDict,
    pension_l_periods: PeriodDict,
) -> PeriodDict:
    print("\n_merge_two_pensions: START")
    date_start_i, date_end_i = _get_pension_dates(itog_periods)
    date_start_l, date_end_l = _get_pension_dates(pension_l_periods)

    print(f" itog range: {date_start_i} — {date_end_i}")
    print(f" pension_l range: {date_start_l} — {date_end_l}")

    combined_periods: list[dict] = []

    if date_start_i <= date_start_l < date_end_i <= date_end_l:
        print(" Branch: date_start_i <= date_start_l < date_end_i <= date_end_l")
        date_start_inter = date_start_l
        date_end_inter = date_end_i

        combined_periods += _periods_before(itog_periods, date_start_inter)

        peresech = _build_result_peresech(
            itog_periods, pension_l_periods, date_start_inter, date_end_inter
        )
        combined_periods += [
            {'date_start': peresech[k]['date_start'],
             'date_end': peresech[k]['date_end'],
             'summa': peresech[k]['summa_3']}
            for k in sorted(peresech.keys())
        ]

        combined_periods += _periods_after(pension_l_periods, date_end_inter)

    elif date_start_l < date_start_i < date_end_l < date_end_i:
        print(" Branch: date_start_l < date_start_i < date_end_l <= date_end_i")
        date_start_inter = date_start_i
        date_end_inter = date_end_l

        combined_periods += _periods_before(pension_l_periods, date_start_inter)

        peresech = _build_result_peresech(
            itog_periods, pension_l_periods, date_start_inter, date_end_inter
        )
        combined_periods += [
            {'date_start': peresech[k]['date_start'],
             'date_end': peresech[k]['date_end'],
             'summa': peresech[k]['summa_3']}
            for k in sorted(peresech.keys())
        ]

        combined_periods += _periods_after(itog_periods, date_end_inter)

    elif (date_start_l <= date_start_i and date_end_i <= date_end_l
          and not (date_start_i >= date_end_l)):
        print(" Branch: l fully covers i (date_start_l <= date_start_i and date_end_i <= date_end_l)")
        date_start_inter = date_start_i
        date_end_inter = date_end_i

        combined_periods += _periods_before(pension_l_periods, date_start_inter)

        peresech = _build_result_peresech(
            itog_periods, pension_l_periods, date_start_inter, date_end_inter
        )
        combined_periods += [
            {'date_start': peresech[k]['date_start'],
             'date_end': peresech[k]['date_end'],
             'summa': peresech[k]['summa_3']}
            for k in sorted(peresech.keys())
        ]

        combined_periods += _periods_after(pension_l_periods, date_end_inter)

    elif (date_start_i <= date_start_l and date_end_l <= date_end_i
          and not (date_start_l >= date_end_i)):
        print(" Branch: i fully covers l (date_start_i <= date_start_l and date_end_l <= date_end_i)")
        date_start_inter = date_start_l
        date_end_inter = date_end_l

        combined_periods += _periods_before(itog_periods, date_start_inter)

        peresech = _build_result_peresech(
            itog_periods, pension_l_periods, date_start_inter, date_end_inter
        )
        combined_periods += [
            {'date_start': peresech[k]['date_start'],
             'date_end': peresech[k]['date_end'],
             'summa': peresech[k]['summa_3']}
            for k in sorted(peresech.keys())
        ]

        combined_periods += _periods_after(itog_periods, date_end_inter)

    elif date_end_i <= date_start_l:
        print(" Branch: itog entirely before pension_l (date_end_i <= date_start_l)")
        for idx in sorted(itog_periods.keys()):
            p = itog_periods[idx]
            combined_periods.append({'date_start': p['date_start'],
                                     'date_end': p['date_end'],
                                     'summa': p['summa']})
            print(f"  append itog as is: {p['date_start']} — {p['date_end']}, {p['summa']}")
        for idx in sorted(pension_l_periods.keys()):
            p = pension_l_periods[idx]
            combined_periods.append({'date_start': p['date_start'],
                                     'date_end': p['date_end'],
                                     'summa': p['summa']})
            print(f"  append pension_l as is: {p['date_start']} — {p['date_end']}, {p['summa']}")

    elif date_end_l <= date_start_i:
        print(" Branch: pension_l entirely before itog (date_end_l <= date_start_i)")
        for idx in sorted(pension_l_periods.keys()):
            p = pension_l_periods[idx]
            combined_periods.append({'date_start': p['date_start'],
                                     'date_end': p['date_end'],
                                     'summa': p['summa']})
            print(f"  append pension_l as is: {p['date_start']} — {p['date_end']}, {p['summa']}")
        for idx in sorted(itog_periods.keys()):
            p = itog_periods[idx]
            combined_periods.append({'date_start': p['date_start'],
                                     'date_end': p['date_end'],
                                     'summa': p['summa']})
            print(f"  append itog as is: {p['date_start']} — {p['date_end']}, {p['summa']}")

    else:
        print(" Branch: no matching condition (возможная пограничная ситуация)")
        # В крайнем случае — просто объединяем все периоды (без дополнительной логики)
        for idx in sorted(itog_periods.keys()):
            p = itog_periods[idx]
            combined_periods.append({'date_start': p['date_start'],
                                     'date_end': p['date_end'],
                                     'summa': p['summa']})
        for idx in sorted(pension_l_periods.keys()):
            p = pension_l_periods[idx]
            combined_periods.append({'date_start': p['date_start'],
                                     'date_end': p['date_end'],
                                     'summa': p['summa']})

    combined_periods.sort(key=lambda p: p['date_start'])
    print(f"_merge_two_pensions: combined_periods count = {len(combined_periods)}")
    for cp in combined_periods:
        print(" ", cp)
    return {idx: period for idx, period in enumerate(combined_periods)}


# Главная функция - рассчитывает итоговые периоды пенсий.
def calculate_pension_itog(pensii_itog_res: dict) -> dict:
    print("\ncalculate_pension_itog: START")
    n_pensions = len(pensii_itog_res)
    print(f" number of pensions = {n_pensions}")

    # Если пенсий нет - ничего не возвращаем и сразу прекращаем
    if n_pensions == 0:
        return {}

    # Шаг 1: ITOG_PENSION0 = список/словарь пенсии 0
    itog: PeriodDict = {}
    print(" initial itog (from pension 0):")
    for k, v in pensii_itog_res[0]['periods'].items():
        itog[k] = {
            'date_start': v['date_start'],
            'date_end': v['date_end'],
            'summa': v['summa'],
        }
        print(f"  {k}: {v['date_start']} — {v['date_end']}, summa={v['summa']}")

    # Шаг 2: Последовательно объединяем с каждой следующей пенсией
    for l in range(1, n_pensions):
        print(f"\nMerging with pension {l} ...")
        pension_l_periods: PeriodDict = {}
        for k, v in pensii_itog_res[l]['periods'].items():
            pension_l_periods[k] = {
                'date_start': v['date_start'],
                'date_end': v['date_end'],
                'summa': v['summa'],
            }
            print(f" pension {l} period {k}: {v['date_start']} — {v['date_end']}, summa={v['summa']}")
        # Объединяем ITOG_PENSION с пенсией l
        itog = _merge_two_pensions(itog, pension_l_periods)
        print(f" after merging with pension {l}, itog has {len(itog)} periods")
        for idx in sorted(itog.keys()):
            p = itog[idx]
            print(f"  itog {idx}: {p['date_start']} — {p['date_end']}, summa={p['summa']}")

    print("calculate_pension_itog: FINISHED\n")
    return itog


if __name__ == '__main__':
    from datetime import date

    pensii_itog_res = {
        0: {
            'type': 'insurance',
            'periods': {
                0: {'date_start': date(2023, 1, 1), 'date_end': date(2023, 10, 1), 'summa': 5000},
            }
        },
        1: {
            'type': 'departmental',
            'periods': {
                0: {'date_start': date(2023, 3, 1), 'date_end': date(2023, 4, 1), 'summa': 6000},
                1: {'date_start': date(2023, 6, 1), 'date_end': date(2023, 8, 6), 'summa': 7000}
            }
        }
    }

    result = calculate_pension_itog(pensii_itog_res)

    print("\n=== ИТОГОВЫЕ ПЕРИОДЫ ПЕНСИЙ ===")
    for idx in sorted(result.keys()):
        p = result[idx]
        print(f"  {idx}: {p['date_start']} — {p['date_end']}: {p['summa']:.2f}")
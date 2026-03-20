from typing import Dict, Any

PeriodDict = Dict[int, Dict[str, Any]]

from src.utils.payments.types.paymentType import PaymentsByPeriods, PeriodAmount, PaymentsByPeriodsItem

def calculate_pension_itog(pensii_itog_res: dict) -> PaymentsByPeriods:
    """
    Агрегирует все пенсии из pensii_itog_res в единый хронологический ряд:
    суммирует суммы всех пенсий для каждого подпериода.
    Возвращает {0: PaymentsByPeriodsItem} — один объединённый результат.
    """
    if not pensii_itog_res:
        return {}

    # Собираем все периоды из всех пенсий в единый список
    all_periods = [
        period
        for pension_data in pensii_itog_res.values()
        for period in pension_data['periods'].values()
    ]

    if not all_periods:
        return {}

    # Все уникальные даты для разбивки на подпериоды
    breakpoints = sorted({
        d
        for p in all_periods
        for d in (p['date_start'], p['date_end'])
    })

    # Для каждого подпериода суммируем суммы всех пенсий, которые его покрывают
    periods_list = []
    for i in range(len(breakpoints) - 1):
        ds = breakpoints[i]
        de = breakpoints[i + 1]

        total = sum(
            p['summa']
            for p in all_periods
            if p['date_start'] <= ds < p['date_end']
        )

        if total > 0:
            periods_list.append(PeriodAmount(DN=ds, DK=de, amount=total))

    # Флаги transferred берём из первой пенсии с is_payment_transferred=True
    transferred = {}
    for pension_data in pensii_itog_res.values():
        t = pension_data.get('transferred', {})
        if t.get('is_payment_transferred', False):
            transferred = t
            break

    return {
        0: PaymentsByPeriodsItem(
            is_payment_transferred=transferred.get('is_payment_transferred', False),
            is_get_PSD_FSD_last_mounth_payment_trasferred=transferred.get('is_get_PSD_FSD_last_mounth_payment_trasferred', False),
            is_get_PSD_FSD_last_year_payment_trasferred=transferred.get('is_get_PSD_FSD_last_year_payment_trasferred', False),
            is_Not_get_PSD_FSD_now_payment_trasferred=transferred.get('is_Not_get_PSD_FSD_now_payment_trasferred', False),
            periods=periods_list,
        )
    }


# def calculate_pension_itog(pensii_itog_res: dict) -> PaymentsByPeriods:
#     if not pensii_itog_res:
#         return {}
    
#     all_periods = [
#         period
#         for pension in pensii_itog_res.values()
#         for period in pension['periods'].values()
#     ]

#     if not all_periods:
#         return {}

#     breakpoints = sorted({
#         d
#         for p in all_periods
#         for d in (p['date_start'], p['date_end'])
#     })
#     print("=" * 80, "breakpoints")

#     print(breakpoints)
#     result: PaymentsByPeriods = {}
#     idx = 0

#     for i in range(len(breakpoints) - 1):
#         ds = breakpoints[i]
#         de = breakpoints[i + 1]

#         total: float = sum(
#             p['summa']
#             for p in all_periods
#             if p['date_start'] <= ds < p['date_end']
#         )
#         print("=" * 80, "total")

#         print(total)
#         if total > 0:
#             result[idx] = {'date_start': ds, 'date_end': de, 'summa': total}
#             idx += 1
        
#         print("=" * 80, "result")

#         print(result)

        

#     return dict(sorted(result.items(), key=lambda kv: kv[1]['date_start']))
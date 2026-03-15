from typing import Dict, Any

PeriodDict = Dict[int, Dict[str, Any]]

from src.utils.payments.types.paymentType import PaymentsByPeriods, PeriodAmount, PaymentsByPeriodsItem

def calculate_pension_itog(pensii_itog_res: dict) -> PaymentsByPeriods:
    """
    Преобразует pensii_itog_res в формат PaymentsByPeriods,
    сохраняя флаги transferred для каждой пенсии и разбивая периоды по брейкпоинтам.
    """
    if not pensii_itog_res:
        return {}
    
    result: PaymentsByPeriods = {}
    
    # Обрабатываем каждую пенсию отдельно
    for pension_key, pension_data in pensii_itog_res.items():
        # Получаем ID пенсии из ключа (например, "pension_0" -> 0)
        pension_id = int(pension_key.split('_')[-1])
        
        # Получаем флаги transferred
        transferred = pension_data.get('transferred', {})
        
        # Получаем все периоды для этой пенсии
        all_periods = list(pension_data['periods'].values())
        
        if not all_periods:
            continue
        
        # Находим все уникальные даты начала и конца периодов
        breakpoints = sorted({
            d
            for p in all_periods
            for d in (p['date_start'], p['date_end'])
        })
        
        # Разбиваем на интервалы и суммируем
        periods_list = []
        for i in range(len(breakpoints) - 1):
            ds = breakpoints[i]
            de = breakpoints[i + 1]
            
            # Суммируем все выплаты, попадающие в этот интервал
            total = sum(
                p['summa']
                for p in all_periods
                if p['date_start'] <= ds < p['date_end']
            )
            
            if total > 0:
                periods_list.append(
                    PeriodAmount(DN=ds, DK=de, amount=total)
                )
        
        # Создаем запись для этой пенсии
        result[pension_id] = PaymentsByPeriodsItem(
            is_payment_transferred=transferred.get('is_payment_transferred', False),
            is_get_PSD_FSD_last_mounth_payment_trasferred=transferred.get('is_get_PSD_FSD_last_mounth_payment_trasferred', False),
            is_get_PSD_FSD_last_year_payment_trasferred=transferred.get('is_get_PSD_FSD_last_year_payment_trasferred', False),
            is_Not_get_PSD_FSD_now_payment_trasferred=transferred.get('is_Not_get_PSD_FSD_now_payment_trasferred', False),
            periods=periods_list
        )
    
    return result


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
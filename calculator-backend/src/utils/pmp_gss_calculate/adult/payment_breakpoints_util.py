from datetime import date, timedelta
from typing import List, Dict, Set, Tuple, Optional
from collections import defaultdict
from src.schemas.json_query_schema import JsonQuerySchema, PaymentInterface
from src.constants.payments_calculate import HOUSIN_AMOUNTS



def get_payment_breakpoints_from_schema(
    data: JsonQuerySchema,
    start_date: date,
    end_date: date
) -> List[date]:
    """
    Формирует список breakpoint'ов на основе данных из JsonQuerySchema
    
    Правила:
    - Для пенсий: только при смене категории пенсии
    - Для EDV, EGDV, EDK: только при смене типа выплаты
    - Для housin: при каждом изменении (даты начала периодов, 
      даты изменения из HOUSIN_AMOUNTS, последняя дата конца)
    """
    breakpoints: Set[date] = set()
    
    # Всегда добавляем начало и конец периода
    breakpoints.add(start_date)
    breakpoints.add(end_date)
    
    payments = data.payments if data.payments else []
    
    if not payments:
        return sorted(breakpoints)
    
    # Группируем выплаты
    grouped = defaultdict(list)
    for payment in payments:
        if payment.type == "pension":
            key = f"pension_{payment.categoria}"
            grouped[key].append(payment)
        else:
            if payment.type in ["housin", "housing"]:
                grouped["housin"].append(payment)
            else:
                grouped[payment.type].append(payment)
    
    # ==================== 1. Обрабатываем ПЕНСИИ ====================
    for key, pension_payments in grouped.items():
        if key.startswith("pension_"):
            sorted_pensions = sorted(pension_payments, key=lambda x: x.DN)
            
            for i, payment in enumerate(sorted_pensions):
                # Добавляем дату начала первой пенсии
                if i == 0:
                    if start_date <= payment.DN <= end_date:
                        breakpoints.add(payment.DN)
                else:
                    prev_payment = sorted_pensions[i - 1]
                    # Проверяем, изменилась ли категория
                    if payment.categoria != prev_payment.categoria:
                        if start_date <= payment.DN <= end_date:
                            breakpoints.add(payment.DN)
                
                # Добавляем дату конца последнего периода
                if i == len(sorted_pensions) - 1:
                    if start_date <= payment.DK <= end_date:
                        breakpoints.add(payment.DK)
    
    # ==================== 2. Обрабатываем EDV, EGDV, EDK ====================
    other_payments = []
    for payment_type in ["edv", "egdv", "edk"]:
        if payment_type in grouped:
            other_payments.extend(grouped[payment_type])
    
    if other_payments:
        # Сортируем по дате начала
        sorted_other = sorted(other_payments, key=lambda x: x.DN)
        
        # Группируем по типу и объединяем периоды
        payments_by_type = defaultdict(list)
        for payment in sorted_other:
            payments_by_type[payment.type].append(payment)
        
        # Объединяем периоды одного типа
        merged_periods = []
        for payment_type, type_payments in payments_by_type.items():
            sorted_type = sorted(type_payments, key=lambda x: x.DN)
            current_start = sorted_type[0].DN
            current_end = sorted_type[0].DK
            
            for p in sorted_type[1:]:
                if p.DN <= current_end:
                    current_end = max(current_end, p.DK)
                else:
                    merged_periods.append((current_start, current_end, payment_type))
                    current_start = p.DN
                    current_end = p.DK
            merged_periods.append((current_start, current_end, payment_type))
        
        # Сортируем по дате начала
        merged_periods.sort(key=lambda x: x[0])
        
        # Находим места смены типа выплаты
        current_type = None
        for period_start, period_end, payment_type in merged_periods:
            if current_type is None:
                # Первый период
                current_type = payment_type
                if start_date <= period_start <= end_date:
                    breakpoints.add(period_start)
            elif payment_type != current_type:
                # Смена типа выплаты
                current_type = payment_type
                if start_date <= period_start <= end_date:
                    breakpoints.add(period_start)
            
            # Добавляем дату конца последнего периода
            if period_end == merged_periods[-1][1]:
                if start_date <= period_end <= end_date:
                    breakpoints.add(period_end)
    
    # ==================== 3. Обрабатываем HOUSIN ====================
    if "housin" in grouped:
        housin_payments = grouped["housin"]
        sorted_housin = sorted(housin_payments, key=lambda x: x.DN)
        
        for i, payment in enumerate(sorted_housin):
            # Добавляем дату начала
            if start_date <= payment.DN <= end_date:
                # Проверяем, не является ли это границей с предыдущим периодом
                if i > 0 and payment.DN == sorted_housin[i-1].DK:
                    # Если начало совпадает с концом предыдущего, не добавляем
                    pass
                else:
                    breakpoints.add(payment.DN)
            
            # Добавляем дату конца, если это не граница со следующим периодом
            if i == len(sorted_housin) - 1:
                # Последний период - добавляем конец
                if start_date <= payment.DK <= end_date:
                    breakpoints.add(payment.DK)
            else:
                next_period = sorted_housin[i + 1]
                if payment.DK != next_period.DN and payment.DK+timedelta(days=1) != next_period.DN:
                    # Если конец не совпадает с началом следующего, добавляем
                    if start_date <= payment.DK <= end_date:
                        breakpoints.add(payment.DK)
        
        # Добавляем даты изменения из HOUSIN_AMOUNTS
        all_housin_change_dates = sorted(HOUSIN_AMOUNTS.keys())
        
        for period in sorted_housin:
            period_start = period.DN
            period_end = period.DK
            
            for change_date in all_housin_change_dates:
                if period_start < change_date < period_end:
                    if start_date <= change_date <= end_date:
                        breakpoints.add(change_date)
    
    return sorted(breakpoints)


from datetime import date, timedelta
from typing import List, Tuple


def split_period_by_breakpoints(
    start_date: date,
    end_date: date,
    breakpoints: List[date]
) -> List[Tuple[date, date]]:
    """
    Разбивает период на подпериоды по брейкпоинтам
    
    Если дата конца подпериода совпадает с датой начала следующего подпериода,
    то дата конца корректируется (вычитается 1 день), чтобы избежать дублирования.
    """
    if not breakpoints:
        return [(start_date, end_date)]
    
    all_points = sorted(set(breakpoints))
    valid_points = [p for p in all_points if start_date <= p <= end_date]
    
    if start_date not in valid_points:
        valid_points.insert(0, start_date)
    if end_date not in valid_points:
        valid_points.append(end_date)
    
    subperiods = []
    for i in range(len(valid_points) - 1):
        sub_start = valid_points[i]
        sub_end = valid_points[i + 1]
        
        # Пропускаем нулевые периоды
        if sub_start >= sub_end:
            continue
        
        # Проверяем, есть ли следующий подпериод
        if i + 1 < len(valid_points) - 1:
            next_start = valid_points[i + 1]
            
            # Если конец текущего периода совпадает с началом следующего
            if sub_end == next_start:
                # Корректируем конец: вычитаем 1 день
                adjusted_end = sub_end - timedelta(days=1)
                
                # Проверяем, что после корректировки период стал больше нуля
                # и не превратился в нулевой период
                if sub_start < adjusted_end:
                    subperiods.append((sub_start, adjusted_end))
                # Если adjusted_end == sub_start, то период нулевой - пропускаем
                # Если adjusted_end < sub_start, тоже пропускаем
            else:
                # Нет совпадения, добавляем как есть
                subperiods.append((sub_start, sub_end))
        else:
            # Последний подпериод - добавляем как есть
            subperiods.append((sub_start, sub_end))
    
    return subperiods

def debug_breakpoints(
    data: JsonQuerySchema,
    start_date: date,
    end_date: date
) -> None:
    """
    Отладочная функция для вывода информации о breakpoint'ах
    """
    breakpoints = get_payment_breakpoints_from_schema(data, start_date, end_date)
    
    print(f"\n=== DEBUG BREAKPOINTS ===")
    print(f"Period: {start_date.strftime('%d.%m.%Y')} - {end_date.strftime('%d.%m.%Y')}")
    print(f"Breakpoints: {[bp.strftime('%d.%m.%Y') for bp in breakpoints]}")
    
    # Показываем выплаты
    if data.payments:
        print(f"\nPayments in schema:")
        for p in data.payments:
            print(f"  {p.type}: {p.DN.strftime('%d.%m.%Y')} - {p.DK.strftime('%d.%m.%Y')} (categoria: {getattr(p, 'categoria', 'N/A')})")
    
    subperiods = split_period_by_breakpoints(start_date, end_date, breakpoints)
    print(f"\nSubperiods:")
    for sub_start, sub_end in subperiods:
        print(f"  {sub_start.strftime('%d.%m.%Y')} - {sub_end.strftime('%d.%m.%Y')}")
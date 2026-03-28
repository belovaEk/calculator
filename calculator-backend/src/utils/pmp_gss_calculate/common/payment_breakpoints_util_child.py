from datetime import date, timedelta
from typing import List, Set, Tuple
from collections import defaultdict
from src.schemas.json_query_schema import JsonQuerySchema
from datetime import date, timedelta
from typing import List, Tuple

from src.utils.logger import logger, log_function_call, log_execution_time

@log_function_call
def get_payment_breakpoints_from_schema_child(
    data: JsonQuerySchema,
    start_date: date,
    end_date: date
) -> List[date]:
    """
    Формирует список breakpoint'ов на основе данных из JsonQuerySchema
    
    Правила:
    Для пенсий: только при смене категории пенсии
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
            logger.warning("Функция get_payment_breakpoints_from_schema_child: ребенку были переданы выплаты с типом отличным от пенсии")
            continue
    
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
    
    return sorted(breakpoints)


def split_period_by_breakpoints_child(
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

def debug_breakpoints_child(
    data: JsonQuerySchema,
    start_date: date,
    end_date: date
) -> None:
    """
    Отладочная функция для вывода информации о breakpoint'ах
    """
    breakpoints = get_payment_breakpoints_from_schema_child(data, start_date, end_date)
    
    print(f"\n=== DEBUG BREAKPOINTS ===")
    print(f"Period: {start_date.strftime('%d.%m.%Y')} - {end_date.strftime('%d.%m.%Y')}")
    print(f"Breakpoints: {[bp.strftime('%d.%m.%Y') for bp in breakpoints]}")
    
    # Показываем выплаты
    if data.payments:
        print(f"\nPayments in schema:")
        for p in data.payments:
            print(f"  {p.type}: {p.DN.strftime('%d.%m.%Y')} - {p.DK.strftime('%d.%m.%Y')} (categoria: {getattr(p, 'categoria', 'N/A')})")
    
    subperiods = split_period_by_breakpoints_child(start_date, end_date, breakpoints)
    print(f"\nSubperiods:")
    for sub_start, sub_end in subperiods:
        print(f"  {sub_start.strftime('%d.%m.%Y')} - {sub_end.strftime('%d.%m.%Y')}")


# ТЕСТЫ
if __name__ == "__main__":
    from datetime import date
    
    # Создаем тестовые данные
    class Payment:
        def __init__(self, type_: str, DN: date, DK: date, categoria: str = None):
            self.type = type_
            self.DN = DN
            self.DK = DK
            self.categoria = categoria
    
    class JsonQuerySchema:
        def __init__(self, payments):
            self.payments = payments
    
    # Тест 1: Пенсии с разными категориями
    payments = [
        Payment("pension", date(2024, 1, 1), date(2024, 6, 30), "insuarance_SPK"),
        Payment("pension", date(2024, 7, 1), date(2024, 12, 31), "social_SPK"),
        Payment("pension", date(2025, 1, 1), date(2025, 3, 31), "social_SPK"),
    ]
    
    data = JsonQuerySchema(payments)
    start_date = date(2024, 1, 1)
    end_date = date(2025, 3, 31)
    
    debug_breakpoints_child(data, start_date, end_date)
    
    # Тест 2: Пустые выплаты
    print("\n" + "="*50)
    data2 = JsonQuerySchema([])
    debug_breakpoints_child(data2, start_date, end_date)
    
    # Тест 3: Только начало и конец
    print("\n" + "="*50)
    payments3 = [
        Payment("pension", date(2024, 3, 1), date(2024, 10, 31), "insuarance_SPK"),
    ]
    data3 = JsonQuerySchema(payments3)
    debug_breakpoints_child(data3, date(2024, 3, 1), date(2024, 10, 31))


    # Тест 4: не пенсии
    payments = [
        Payment("egdv", date(2024, 1, 1), date(2024, 6, 30), "gosudarstvennaya_disability"),
        Payment("egdv", date(2024, 7, 1), date(2024, 12, 31), "departmental_age"),
        Payment("edv", date(2025, 1, 1), date(2025, 3, 31), "departmental_age"),
    ]
    
    data4 = JsonQuerySchema(payments)
    start_date = date(2024, 1, 1)
    end_date = date(2025, 3, 31)
    
    debug_breakpoints_child(data4, start_date, end_date)
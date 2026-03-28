from datetime import datetime, timedelta, date
from typing import List
from src.utils.pmp_gss_calculate.type import GssPmpPensionType
from src.schemas.json_query_schema import OrderType, PeriodWithIdType, PeriodType
from dateutil.relativedelta import relativedelta


async def cut_off_periods_before_change_date(
    periods: List[PeriodWithIdType],
    change_last_date: date,
) -> List[PeriodWithIdType]:
    """
    Отсекает все периоды стационаризации, которые полностью
    находятся до даты последнего изменения данных в выплате,
    и обрезает периоды, начавшиеся до этой даты.

    Цель соответствует схеме: оставить только ту часть периода
    нахождения в стационарном учреждении, которая идет после
    даты последнего изменения данных в выплате.
    """
    if not periods:
        return []

    new_periods_inpatient: List[PeriodWithIdType] = []
    
    for period in periods:

        DN = period.DN
        DK = period.DK

        if change_last_date <= DN < DK:
            new_periods_inpatient.append(PeriodWithIdType(id=period.id, DN=DN, DK=DK))
        elif DN <= change_last_date < DK:
            new_periods_inpatient.append(PeriodWithIdType(id=period.id, DN=change_last_date, DK=DK))


        # # Если стационар закончился до или в дату изменения выплаты — пропускаем
        # if period.DK <= change_last_date:
        #     continue

        # # Новая дата начала — максимум из DN и даты изменения выплаты
        # new_dn = max(period.DN, change_last_date)
        # new_dk = period.DK

        # # Защита от вырожденных периодов
        # if new_dn < new_dk:
        #     result.append(PeriodType(DN=new_dn, DK=new_dk))

    return new_periods_inpatient



async def cut_of_order_date(orders_date: List[OrderType],  change_last_date: date) -> List[OrderType]:
    """ Отсекает все даты подачи заявлений на ГСС до даты внесения изменений в данные выплаты

    Args:
        order_date (List[OrderType]): даты подачи заявления

    Returns:
        List[OrderType]: даты подачи заявления до даты внесения изменений в данные выплаты
    """    
    if not orders_date:
        return []
    
    new_order_date: List[OrderType] = []

    for order in orders_date:
        date = order.date 
        if date >= change_last_date:
            new_order_date.append(OrderType(id=order.id, date=order.date))

    return new_order_date

# Добавьте эту функцию в файл cut_off_periods_util.py перед функцией cut_of_gss_no_have_order

async def merge_periods(periods):
    """Объединяет пересекающиеся периоды"""
    if not periods:
        return []
    
    # Сортируем периоды по дате начала
    periods.sort(key=lambda x: x.DN)
    
    merged = []
    current = periods[0]
    
    for period in periods[1:]:
        # Если текущий период пересекается или соприкасается со следующим
        if current.DK >= period.DN:
            # Объединяем
            current = PeriodType(
                DN=current.DN,
                DK=max(current.DK, period.DK)
            )
        else:
            # Добавляем текущий в результат и начинаем новый
            merged.append(current)
            current = period
    
    # Добавляем последний период
    merged.append(current)
    
    return merged

async def cut_of_gss_no_have_order(
    gss_period: List[PeriodWithIdType], 
    pmp_periods: List[PeriodWithIdType], 
    orders_date: List[OrderType]
):
    """ 
    Убирает все периоды ГСС, на которые не подавалось заявление от гражданина (переводит в ПМП)
    - ПМП период заканчивается последним днем месяца, предшествующего дате заявления
    - ГСС начинается с 1 числа следующего месяца после даты заявления
    """
    
    # Сортируем
    gss_period.sort(key=lambda x: x.DN)
    pmp_periods.sort(key=lambda x: x.DN)
    
    new_gss_periods = []
    new_pmp_periods = pmp_periods.copy()
    
    def get_last_day_of_previous_month(date):
        """Возвращает последний день месяца, предшествующего дате"""
        # Первый день следующего месяца минус 1 день
        first_day_current_month = date.replace(day=1)+ relativedelta(months=1)
        return first_day_current_month - timedelta(days=1)
    
    def get_first_day_next_month(date):
        """Возвращает 1 число следующего месяца"""
        return (date.replace(day=1) + relativedelta(months=1))
    
    for period in gss_period:
        period_start = period.DN
        period_end = period.DK
        
        # Проверяем, есть ли заявление в этом периоде
        orders_in_period = [
            order.date for order in orders_date 
            if period_start <= order.date < period_end
        ]
        orders_in_period.sort()
        
        if orders_in_period:
            # Есть заявления - разбиваем период
            current_start = period_start
            
            for order_date in orders_in_period:
                if current_start < order_date:
                    # Часть ДО заявления - ПМП
                    # ПМП заканчивается последним днем месяца, предшествующего дате заявления
                    pmp_end = get_last_day_of_previous_month(order_date)
                    
                    # Проверяем, что дата окончания ПМП не раньше даты начала
                    if pmp_end >= current_start:
                        new_pmp_periods.append(PeriodType(
                            DN=current_start, 
                            DK=pmp_end
                        ))
                        current_start = pmp_end + timedelta(days=1)
                
                # Часть ПОСЛЕ заявления - ГСС, начиная с 1 числа следующего месяца
                gss_start = get_first_day_next_month(order_date)
                
                # Если дата начала ГСС не выходит за пределы периода
                if gss_start <= period_end:
                    current_start = gss_start
                else:
                    # Если ГСС начинается после окончания периода
                    current_start = order_date
            
            # Добавляем оставшуюся часть периода (если есть)
            if current_start < period_end:
                # Проверяем, является ли оставшаяся часть ГСС
                # Если current_start - это дата начала ГСС или позже
                if current_start > period_start:
                    new_gss_periods.append(PeriodType(
                        DN=current_start, 
                        DK=period_end
                    ))
                else:
                    # Иначе это ПМП
                    new_pmp_periods.append(PeriodType(
                        DN=current_start, 
                        DK=period_end
                    ))
        else:
            # Нет заявления в периоде
            # Проверяем, есть ли ПМП период, который пересекается с этим периодом
            has_pmp_overlap = any(
                pmp.DK > period_start for pmp in pmp_periods
            )
            
            # Проверяем, есть ли заявление после этого периода
            has_order_after = any(
                order.date >= period_end for order in orders_date
            ) if orders_date else False
            
            # Если есть ПМП до/во время периода ИЛИ нет заявлений после - переводим в ПМП
            if has_pmp_overlap or not has_order_after:
                new_pmp_periods.append(PeriodType(DN=period_start, DK=period_end))
            else:
                # Иначе оставляем в ГСС
                new_gss_periods.append(PeriodType(DN=period_start, DK=period_end))
    
    # Объединяем пересекающиеся периоды
    new_pmp_periods = await merge_periods(new_pmp_periods)
    new_gss_periods = await merge_periods(new_gss_periods)
    
    return {
        "pmp_periods": new_pmp_periods,
        "gss_periods": new_gss_periods
    }    
            

async def adjust_employment_periods(employment_periods: List[PeriodType]) -> List[PeriodType]:
    """Преобразует даты трудоустройства в 1 число следующего месяца"""
    adjusted = []
    for emp in employment_periods:
        adjusted.append(PeriodType(
            id=emp.id if hasattr(emp, 'id') else None,
            DN=(emp.DN.replace(day=1) + relativedelta(months=1)),
            DK=(emp.DK.replace(day=1) + relativedelta(months=1))
        ))
    return adjusted
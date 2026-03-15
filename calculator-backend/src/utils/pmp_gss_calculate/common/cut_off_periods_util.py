from datetime import date
from typing import List
from src.utils.pmp_gss_calculate.type import GssPmpPensionType
from src.schemas.json_query_schema import OrderType, PeriodWithIdType, PeriodType
from src.utils.pmp_gss_calculate.common.merge_periods_util import merge_periods


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
        if date > change_last_date:
            new_order_date.append(OrderType(id=order.id, date=order.date))

    return new_order_date



async def cut_of_gss_no_have_order(gss_period: List[PeriodWithIdType], pmp_periods: List[PeriodWithIdType], orders_date: List[OrderType]):
    """ Убирает все периоды ГСС, на которые не подавалось заявление от гражданина (переводит в ПМП)

    Args:
        gss_period (List[PeriodWithIdType]): периоды ГСС
        pmp_periods (List[PeriodWithIdType]): Периоды ПМП
        orders_date (List[OrderType]): Заявления на ГСС

    Returns:
        Возвращает словарь:
        {
        "pmp_periods" (GssPmpPensionType),
        "gss_periods" (GssPmpPensionType)
        }
          
    """   
    
    gss_period.sort(key=lambda x: x.DN)
    pmp_periods.sort(key=lambda x: x.DN)
    new_gss_periods: GssPmpPensionType = {}
    new_pmp_periods: GssPmpPensionType = {}

    new_gss_periods[0] = [] # загулшка для типа индекс пенсии
    new_pmp_periods[0] = pmp_periods 

    for i in range(len(orders_date)):
        current_order = orders_date[i]
        date_order = current_order.date
        
        for j in range(len(gss_period)):
            current_period = gss_period[j]
            
            if j == 0 and len(pmp_periods) > 0:
                if not(pmp_periods[0].DK < current_period.DK):
                    new_gss_periods[0].append(PeriodType(DN=current_period.DN, DK=current_period.DK))
                    break

            if current_period.DN <= date_order < current_period.DK:
                new_gss_periods[0].append(PeriodType(DN=date_order, DK=current_period.DK))

                if current_period.DN != date_order:
                    new_pmp_periods[0].append(PeriodType(DN=current_period.DN, DK=date_order))

            elif date_order < current_period.DN:
                new_gss_periods[0].append(PeriodType(DN=current_period.DN, DK=current_period.DK))
            
            else:
                new_pmp_periods[0].append(PeriodType(DN=current_period.DN, DK=current_period.DK))

    return {
        "pmp_periods": new_pmp_periods,
        "gss_periods": new_gss_periods
    }       
                        
            


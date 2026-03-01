from src.schemas.json_query_schema import (
    JsonQuerySchema,
    PeriodType,
)
from datetime import date
from dateutil.relativedelta import relativedelta
from typing import List
from src.utils.payment_util import (
    get_date_init_pension_Moscow,
    
)

from src.utils.registration.registration_util import (
    calculate_registration_summary,
    breadwinner_or_representative_date10,
    calculate_total_registration_without_breaks,
)

from src.utils.auxiliary_util import sort_periods_in_data, is_adult
from src.utils.pmp_gss_calculate.prepare_pmp_gss_result import prepare_pmp_gss_result


# Главная функция для расчета
async def main_util(data: JsonQuerySchema) -> dict:
    """
    Главная вызываемая функция, точка входа в весь алгоритм.
    Имеет основную логику алгоритма, и использует другие функции для реализации каждого шага.
    """
    # Инициализация основных переменных
    today = date.today()
    spv_init_date = await get_date_init_pension_Moscow(data.payments)  # Дата первой пенсии в Москве
    sum_reg_10_date = None  # Дата наступления 10 лет суммарной регистрации в Москве
    pmp_periods: List[PeriodType] = []  # Периоды прожиточного минимума пенсионера
    gss_periods: List[PeriodType] = []  # Периоды городского социального стандарта

    # Препроцессинг: сортировка полей периодов в data и валидация 
    data = sort_periods_in_data(data=data)

    # Проверка возраста
    # Алгоритм работает только с несовершеннолетними (дети)
    if await is_adult(today=today, date_of_birth=data.date_of_birth):
        return {"message": "Взрослые не обрабатываются"}

    # Проверка, что с даты первичного назначения СПВ прошло больше 1 месяца
    spv_delta = relativedelta(today, spv_init_date)
    if spv_delta.years == 0 and spv_delta.months == 0:
        return {"message": "С даты первичного назначения СПВ прошло меньше 1 месяца"}

    # Проверка наличия регистрации в Москве
    if not data.is_there_a_registration_in_moscow:
        return {"message": "Нет регистрации в Москве"}

    # Получаем периоды регистрации ребенка
    list_of_periods_reg_child = data.periods_reg_moscow
    
    # Рассчитываем суммарный срок регистрации и дату последнего разрыва
    summary_registration = await calculate_registration_summary(
        list_of_periods_reg=list_of_periods_reg_child
    )

    # ОСНОВНАЯ ЛОГИКА ОПРЕДЕЛЕНИЯ ДАТЫ 10 ЛЕТ
    if summary_registration["total_period"].years > 10:
        # Случай 1: У ребенка более 10 лет суммарной регистрации
        registration_result = await calculate_total_registration_without_breaks(
            data.periods_reg_moscow
        )
        if registration_result["has_10_years"]:
            sum_reg_10_date = registration_result["date_of_10_years"]
    
    elif (summary_registration["last_break_date"] 
          and summary_registration["last_break_date"] < data.date_of_birth + relativedelta(months=6)
          and summary_registration["last_break_date"] < spv_init_date):
        # Случай 2: Сработало условие с датой последнего разрыва
        sum_reg_10_date = summary_registration["last_break_date"]
    
    else:
        # Случай 3: Проверка через кормильца или представителя
        sum_reg_10_date = await breadwinner_or_representative_date10(data=data, today=today)
    
    # ОБЩИЙ БЛОК: Если дата найдена, формируем периоды ПМП и ГСС
    if sum_reg_10_date:
        return await prepare_pmp_gss_result(
            data=data,
            sum_reg_10_date=sum_reg_10_date,
            spv_init_date=spv_init_date,
            list_of_periods_reg_child=list_of_periods_reg_child,
            pmp_periods=pmp_periods,
            gss_periods=gss_periods
        )
    
    # Если ни одно условие не выполнилось
    return {
        "message": "Положено РСД до ПМП с даты назначения пенсии до окончания срока выплаты"
    }


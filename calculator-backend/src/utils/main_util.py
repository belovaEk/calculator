from fastapi.background import P
from src.schemas.json_query_schema import (
    JsonQuerySchema,
    PeriodType,
    PaymentInterface,
)
from datetime import date
from dateutil.relativedelta import relativedelta
from typing import List
from src.utils.calculate_util import (
    is_adult,
    get_date_init_pension_Moscow,
    calculate_registration_summary,
    breadwinner_or_representative,
    calculate_total_registration_without_breaks
)
from src.utils.auxiliary_util import PMP_GSS_primal, sort_periods_in_data


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

    # Проверка достижения 10 лет суммарной регистрации ребенка
    if summary_registration["total_period"].years > 10:
        # Достигнуто более 10 лет - вычисляем точную дату достижения
        registration_result = await calculate_total_registration_without_breaks(
            data.periods_reg_moscow
        )

        if registration_result["has_10_years"]:
            sum_reg_10_date = registration_result["date_of_10_years"]

            # Разделение на периоды ПМП и ГСС
            # В зависимости от соотношения дат ДР10 и даты первой пенсии
            pmp_gss_result = await PMP_GSS_primal(sum_reg_10_date, spv_init_date, list_of_periods_reg_child, PMP=pmp_periods, GSS=gss_periods)

            pmp_periods = pmp_gss_result["PMP"]
            gss_periods = pmp_gss_result["GSS"]

            # Возвращаем результат с датой и периодами
            # ОТЛАДОЧНЫЙ ВЫВОД
            return {
                "date_of_10_years_child": sum_reg_10_date,
                "list_of_periods_reg_child": list_of_periods_reg_child,
                "pmp_periods": pmp_periods,
                "gss_periods": gss_periods
            }

    else:
        # Меньше 10 лет суммарной регистрации
        dn_reg_m = summary_registration["last_break_date"]
        
        # Условие: дата последнего разрыва должна быть:
        # 1. меньше даты рождения + 6 месяцев
        # 2. меньше даты первой пенсии
        if (
            dn_reg_m
            and dn_reg_m < data.date_of_birth + relativedelta(months=6)
            and dn_reg_m < spv_init_date
        ):
            sum_reg_10_date = dn_reg_m

            # Разделение на периоды ПМП и ГСС
            # В зависимости от соотношения дат ДР10 и даты первой пенсии
            pmp_gss_result = await PMP_GSS_primal(sum_reg_10_date, spv_init_date, list_of_periods_reg_child, PMP=pmp_periods, GSS=gss_periods)

            pmp_periods = pmp_gss_result["PMP"]
            gss_periods = pmp_gss_result["GSS"]

            # Возвращаем результат с датой и периодами
            # ОТЛАДОЧНЫЙ ВЫВОД
            return {
                "date_of_10_years_child": sum_reg_10_date,
                "list_of_periods_reg_child": list_of_periods_reg_child,
                "pmp_periods": pmp_periods,
                "gss_periods": gss_periods
            }

        # Если ребенок не набрал 10 лет, проверяем кормильца или представителя
        breadwinner_result = await breadwinner_or_representative(data=data, today=today)

        if breadwinner_result:
            sum_reg_10_date = breadwinner_result

            # Разделение на периоды ПМП и ГСС
            # В зависимости от соотношения дат ДР10 и даты первой пенсии
            pmp_gss_result = await PMP_GSS_primal(sum_reg_10_date, spv_init_date, list_of_periods_reg_child, PMP=pmp_periods, GSS=gss_periods)

            pmp_periods = pmp_gss_result["PMP"]
            gss_periods = pmp_gss_result["GSS"]

            # Возвращаем результат с датой и периодами
            # ОТЛАДОЧНЫЙ ВЫВОД
            return {
                "date_of_10_years": sum_reg_10_date,
                "list_of_periods_reg": list_of_periods_reg_child,
                "pmp_periods": pmp_periods,
                "gss_periods": gss_periods
            }

        # Если ни одно условие не выполнилось возвращаем стандартное сообщение о положенной выплате
        return {
            "message": "Положено РСД до ПМП с даты назначения пенсии до окончания срока выплаты"
        }
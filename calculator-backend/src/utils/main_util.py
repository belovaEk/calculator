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
from src.utils.auxiliary_util import PMP_GSS_primal


# Главная функция для расчета
async def main_util(data: JsonQuerySchema) -> dict:
    '''
    Главная вызываемая функция, точка входа в весь алгоритм.
    Имеет основную логику алгоритма, и использует другие функции для реализации каждого шага.
    '''
    today = date.today()
    spv_init_date = await get_date_init_pension_Moscow(data.payments)
    sum_reg_10_date = None  # Дата наступления 10 лет регистрации в Москве

    # Проверка возраста
    if await is_adult(today=today, date_of_birth=data.date_of_birth) == True:
        return {"Взрослые не обрабатываются"}

    # # Проверка, что с даты первичного назначения СПВ прошло больше 1 месяца
    # spv_delta = relativedelta(today, spv_init_date)
    # # Проверяем, прошло ли меньше 1 месяца
    # if spv_delta.years == 0 and spv_delta.months == 0:
    #     return {"С даты первичного назначения СПВ прошло меньше 1 месяца"}

    # Есть ли регистрация в Москве?
    if data.is_there_a_registration_in_moscow == True:
        list_of_periods_reg_child = data.periods_reg_moscow
        summary_registration = await calculate_registration_summary(
            list_of_periods_reg= list_of_periods_reg_child
        )

        if summary_registration["total_period"].years > 10:
            result = await calculate_total_registration_without_breaks(data.periods_reg_moscow)
            
            if result["has_10_years"] == True:
                sum_reg_10_date = result["date_of_10_years"]
                PMP_GSS_primal()
                return {f"Дата 10 лет у ребенка: {sum_reg_10_date}"}

        else:
            DNregM = summary_registration["last_break_date"]
            if (
                DNregM < data.date_of_birth + relativedelta(months=6)
                and DNregM
                and DNregM < spv_init_date
            ):
                sum_reg_10_date = DNregM
                return {f"10 лет регистрации: {sum_reg_10_date}"}
            else:
                result = await breadwinner_or_representative(data=data, today=today)
                print(result)
                if result:
                    return {f"Дата 10 лет: {result}"}
                return {
                    "Вывод: положено РСД до ПМП с даты назначения пенсии до окончания срока выплаты"
                }

    return {"end": True}

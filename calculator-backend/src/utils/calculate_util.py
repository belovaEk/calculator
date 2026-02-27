from src.schemas.json_query_schema import JsonQuerySchema, RegistrationPeriod
from datetime import date
from dateutil.relativedelta import relativedelta
from typing import List


today = date.today()


async def is_adult(today, date_of_birth):
    delta = relativedelta(today, date_of_birth)
    if delta.years >= 18:
        return True
    return False


async def is_sum_of_periods_of_registration_more_than_10_years(list_of_periods: List[RegistrationPeriod]):

    sum_of_periods = relativedelta()

    for period in list_of_periods:

        delta = relativedelta(period.DK, period.DN)
        sum_of_periods += delta

    if delta.years > 10:
        return True
    else:
        return False


async def is_sum_of_periods_of_registration_more_than_10_years_and_no_defference_more_than_1_month(list_of_periods: List[RegistrationPeriod]):
    
    sum_of_periods = relativedelta()

    for i in range(len(list_of_periods)):
        if i > 0:
            prev_end = list_of_periods[i-1].DKreg
            curr_start = list_of_periods[i].DNreg
            if relativedelta(curr_start, prev_end).months > 1 or relativedelta(curr_start, prev_end).years > 0:
                sum_of_periods = relativedelta()
        
        delta = relativedelta(list_of_periods[i].DKreg, list_of_periods[i].DNreg)
        sum_of_periods += delta

    if delta.years > 10:
        return True
    else:
        return False


# Проверяет: текущая дата - дата первичного назначения СПВ у> 1 месяца?
async def is_the_difference_between_the_current_date_and_the_date_of_the_initial_appointment_of_the_SPV_more_than_1_month(today, data: JsonQuerySchema):

    today = date.today()
    appointment_date = data.date_of_the_initial_appointment_of_the_SPV_is_137_or_143

    delta = relativedelta(today, appointment_date)

    # Проверяем, прошло ли больше месяца
    if delta.months > 0 or delta.years > 0:
        return True
    else:
        return False







# Главная функция для расчета 
async def calculate_util(data: JsonQuerySchema) -> dict:

    today = date.today()

    # Проверка возраста
    if await is_adult(today=today, date_of_birth=data.date_of_birth) == True:
        return {"Взрослые не обрабатываются"}

    # Проверка, что с даты первичного назначения СПВ прошло больше 1 месяца
    if await is_the_difference_between_the_current_date_and_the_date_of_the_initial_appointment_of_the_SPV_more_than_1_month(today=today, data=data) == False:
        return {"С даты первичного назначения СПВ прошло меньше 1 месяца"}

    # Вид социальной выплаты = страховая пенсия по СПК?
    if data.type_of_social_payment.lower() == "страховая пенсия по спк":
        if data.is_there_a_registration_in_moscow == True:
            list_of_periods_child=data.the_periods_of_registration_in_moscow_of_the_child

            if await is_sum_of_periods_of_registration_more_than_10_years_and_no_defference_more_than_1_month(list_of_periods=list_of_periods_child) == True:
                return {"Суммарная дата регистрации больше 10 лет"}
            else:
                if data.periods_of_registration_in_moscow[0].DN + relativedelta(months=6) <= today:
                    pass

                return {"Суммарная дата регистрации меньше 10 лет"}
        else: 
            return {"Вы не зарегистрированы в Москве"}

    # # Вид социальной выплаты = социальная пенсия по инвалидности?
    elif data.type_of_social_payment.lower() == "социальная пенсия по инвалидности":
        return {"социальная пенсия по инвалидности в разработке"}

    return {"end": True}


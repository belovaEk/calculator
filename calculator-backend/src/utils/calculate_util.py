from src.schemas.json_query_schema import JsonQuerySchema, RegistrationPeriod, PaymentInterface
from datetime import date
from dateutil.relativedelta import relativedelta
from typing import List


async def is_adult(today, date_of_birth):
    delta = relativedelta(today, date_of_birth)
    if delta.years >= 18:
        return True
    return False


async def calculate_registration_summary(list_of_periods: List[RegistrationPeriod]):
    '''
    Возвращает суммарый срок регистрации в Москве и дату начала первого периода регистрации 
    (дату начала периода регистрации после разрыва в более, чем 1 месяц)
    '''
    if not list_of_periods:
        return {
            "total_period": relativedelta(),
            "last_break_date": None
        }

    sum_of_periods = relativedelta()
    break_dates = []
    current_sum = relativedelta()
    
    for i in range(len(list_of_periods)):
        if i > 0:
            prev_end = list_of_periods[i-1].DK
            curr_start = list_of_periods[i].DN
            if relativedelta(curr_start, prev_end).months > 1 or relativedelta(curr_start, prev_end).years > 0:
                break_dates.append(list_of_periods[i].DN)
                current_sum = relativedelta()
        
        delta = relativedelta(list_of_periods[i].DK, list_of_periods[i].DN)
        current_sum += delta
        sum_of_periods += delta
    
    return {
        "total_period": sum_of_periods,
        "last_break_date": break_dates[-1] if break_dates else list_of_periods[0].DN
    }


async def get_date_init_pension_Moscow(payments: List[PaymentInterface]):
    '''
    Возвращает дату назначения первой пенсии в Москве
    '''
    for payment in payments:
        if payment.is_Moscow and payment.type == 'pension':
            return payment.DN
    return None






# Главная функция для расчета 
async def calculate_util(data: JsonQuerySchema) -> dict:

    today = date.today()
    spv_init_date = await get_date_init_pension_Moscow(data.payments)
    print(spv_init_date)
    DR10 = None  # Дата наступления 10 лет регистрации в Москве

    # Проверка возраста
    if await is_adult(today=today, date_of_birth=data.date_of_birth) == True:
        return {"Взрослые не обрабатываются"}

    # Проверка, что с даты первичного назначения СПВ прошло больше 1 месяца
    spv_delta = relativedelta(today, spv_init_date)
    # Проверяем, прошло ли меньше 1 месяца
    if spv_delta.years == 0 and spv_delta.months == 0:
        return {"С даты первичного назначения СПВ прошло меньше 1 месяца"}

    # Есть ли регистрация в Москве?
    if data.is_there_a_registration_in_moscow == True:
        list_of_periods_child=data.periods_of_registration_in_moscow

        summary_registration = await calculate_registration_summary(list_of_periods=list_of_periods_child)
        if summary_registration["total_period"].years > 10:
            return {"Суммарная дата регистрации больше 10 лет. Идем по алгоритму далее"}
        else:
            DNregM = summary_registration["last_break_date"]
            if DNregM < data.date_of_birth + relativedelta(months=6) and DNregM and DNregM < spv_init_date:
                DR10 = DNregM
                return {
                    f"10 лет регистрации: {DR10}"
                }
            else:
                return {
                    "Требуются периоды регистрации в Москве кормильца/ законного представителя"
                }
    else: 
        return {"Вывод: положено РСД до ПМП с даты назначения пенсии до окончания срока выплаты"}

    return {"end": True}


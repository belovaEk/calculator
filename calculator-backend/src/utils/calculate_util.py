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
    # Добавить сортировку периодов и выбирать с ранней датой
    for payment in payments:
        if payment.is_Moscow and payment.type == 'pension':
            return payment.DN
    return None









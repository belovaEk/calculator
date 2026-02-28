from src.schemas.json_query_schema import (
    JsonQuerySchema,
    RegistrationPeriod,
    PaymentInterface,
    PeriodDuration
)
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from typing import List


async def is_adult(today, date_of_birth):
    delta = relativedelta(today, date_of_birth)
    if delta.years >= 18:
        return True
    return False


async def calculate_registration_summary(list_of_periods: List[RegistrationPeriod]):
    """
    Возвращает суммарый срок регистрации в Москве и дату начала первого периода регистрации
    (дату начала периода регистрации после разрыва в более, чем 1 месяц)
    """
    if not list_of_periods:
        return {"total_period": relativedelta(), "last_break_date": None}

    sum_of_periods = relativedelta()
    break_dates = []
    current_sum = relativedelta()

    for i in range(len(list_of_periods)):
        if i > 0:
            prev_end = list_of_periods[i - 1].DK
            print(prev_end)
            curr_start = list_of_periods[i].DN
            if (
                relativedelta(curr_start, prev_end).months > 1
                or relativedelta(curr_start, prev_end).years > 0
            ):
                break_dates.append(list_of_periods[i].DN)
                current_sum = relativedelta()
        delta = relativedelta(list_of_periods[i].DK, list_of_periods[i].DN)
        current_sum += delta
        sum_of_periods += delta

    return {
        "total_period": sum_of_periods,
        "last_break_date": break_dates[-1] if break_dates else list_of_periods[0].DN,
    }


async def get_date_init_pension_Moscow(payments: List[PaymentInterface]):
    """
    Возвращает дату назначения первой пенсии в Москве
    """
    # Добавить сортировку периодов и выбирать с ранней датой
    for payment in payments:
        if payment.is_Moscow and payment.type == "pension":
            return payment.DN
    return None


def calculate_exact_duration(start_date: date, end_date: date) -> PeriodDuration:
    """Вычисляет точную продолжительность периода с учетом лет, месяцев и дней"""
    delta = relativedelta(end_date, start_date)
    return PeriodDuration.from_relativedelta(delta)


async def calculate_total_registration_without_breaks(
    list_of_periods: List[RegistrationPeriod],
) -> dict:
    """
    Возвращает информацию о достижении 10 лет суммарной регистрации в Москве
    без обнуления счетчика при разрывах (суммируются все периоды подряд)
    """
    if not list_of_periods:
        return {"has_10_years": False, "date_of_10_years": None}

    total_duration = PeriodDuration()
    ten_years = PeriodDuration(years=10)
    
    for period in list_of_periods:
        period_duration = calculate_exact_duration(period.DN, period.DK)
        
        # Проверяем, достигается ли 10 лет в этом периоде
        remaining_to_10 = ten_years - total_duration
        
        # Преобразуем в relativedelta для сравнения
        remaining_rd = remaining_to_10.to_relativedelta()
        
        if (period.DN + remaining_rd) <= period.DK:
            date_of_10_years = period.DN + remaining_rd
            return {"has_10_years": True, "date_of_10_years": date_of_10_years}
        
        total_duration += period_duration
    
    return {"has_10_years": False, "date_of_10_years": None}



# async def calculate_total_registration_without_breaks(
#     list_of_periods: List[RegistrationPeriod],
# ):
#     """
#     Возвращает информацию о достижении 10 лет суммарной регистрации в Москве
#     без обнуления счетчика при разрывах (суммируются все периоды подряд)
#     """
#     if not list_of_periods:
#         return {"has_10_years": False, "date_of_10_years": None}

#     total = relativedelta()
#     ten_years = relativedelta(years=10)

#     my_date = date(2024, 12, 31)  
#     today = date.today()

    
#     for period in list_of_periods:
#         period_delta = relativedelta(period.DK, period.DN)

#         # Сравниваем через преобразование в порядковый номер дня
#         if (period.DN + (ten_years - total)) <= period.DK:
#             # Нашли период, в котором достигается 10 лет суммарно
#             date_of_10_years = period.DN + (ten_years - total)
#             return {"has_10_years": True, "date_of_10_years": date_of_10_years}
        
#         total += period_delta

#     return {"has_10_years": False, "date_of_10_years": None}


async def breadwinner_or_representative(data: JsonQuerySchema, today: date):
    """
    Сначала проверяет, что у представителя есть актуальная на сегодняшний день регистрация в Москве, далее
    проверяет представиля на наличие суммарной регистрации в 10 лет.
    Если условия не выполнились, проверяет была ли у кормильца на момент смерти регистрация в Москве,
    если была то тоже проверяет на наличие суммарной регистрации в 10 лет.
    """

    # Если есть законный представитель, и у него есть актуальная регистрация в Москве
    if data.periods_reg_representative_moscow:

        result = await calculate_total_registration_without_breaks(
            data.periods_reg_representative_moscow
        )
        
        if (
            data.periods_reg_representative_moscow[-1].DK == today
            and result["has_10_years"] == True
        ):
            return result["date_of_10_years"]

    if data.periods_reg_breadwinner_moscow:

        result = await calculate_total_registration_without_breaks(
            data.periods_reg_breadwinner_moscow
        )
        print(result)
        if (
            data.periods_reg_breadwinner_moscow[-1].DK == data.date_of_death_of_the_breadwinner
            and result["has_10_years"] == True
        ):
            return result["date_of_10_years"]

    return None

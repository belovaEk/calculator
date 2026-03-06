from src.constants.payment_const import SOCIAL_PENSION_INDEX, INSURANCE_PENSION_SCORE, INSURANCE_PENSION_FIX_AMOUNT
from datetime import date
from typing import  Dict, List

from src.utils.payments.types.paymentType import PaymentsByYear
from src.schemas.json_query_schema import (
    JsonQuerySchema, PaymentInterface, PeriodType
)

def get_score_fix_amount_insurance(DNpen: date):
    target_score = 0
    target_fix_amount = 0
    
    for current_date, score in INSURANCE_PENSION_SCORE.items():
        if current_date <= DNpen:
            target_score = score
            target_fix_amount = INSURANCE_PENSION_FIX_AMOUNT[current_date]
        else:
            break
    return {
            'score': target_score,
            'fix_amount': target_fix_amount
        }


async def calculate_sp_standart(data: JsonQuerySchema) -> PaymentsByYear:
    """ Функция по расчета стандартных выплат пенсии по годам

    Returns:
        PaymentsByYear: Возвращает словаь с индексом пенсии, которому принадлежит словарь с годами и соотвествующими стандартными выплатами
    """    

    pensions = [p for p in data.payments if p.type == 'pension']
    print(43)
    sp_standart_by_year: PaymentsByYear = {}

    for pension in pensions:

        if pension.categoria == "insurance_SPK":
            sp_standart_by_year = await pension_insurance_SPK_calculate(data=data, pension=pension, sp_standart_by_year=sp_standart_by_year)
        elif pension.categoria == "social_SPK" or pension.categoria == "social_disability":
            sp_standart_by_year = await pension_social_calculate(data=data, pension=pension, sp_standart_by_year=sp_standart_by_year)
        elif pension.categoria == "departmental":
            sp_standart_by_year = await pension_departmental_calculate(pension=pension, sp_standart_by_year=sp_standart_by_year)
    return sp_standart_by_year
    


async def pension_insurance_SPK_calculate(data: JsonQuerySchema, pension: PaymentInterface, sp_standart_by_year) -> PaymentsByYear:

    """ Функция по расчета стандартных выплат по страховой пенсии по годам

    Returns:
        PaymentsByYear: Возвращает словаь с индексом пенсии, которому принадлежит словарь с годами и соотвествующими стандартными выплатами
    """ 

    DNpen = pension.DN
    DKpen = pension.DK
    year = DNpen.year
    summa = pension.amount

    score_fix = get_score_fix_amount_insurance(DNpen)
    score = score_fix['score']
    fix_amount = score_fix['fix_amount'] / 2

    sp_standart_by_year[pension.id] = {}

    isRSD = True

    if (score != 0 and fix_amount != 0):
        IPK = (pension.amount - (fix_amount / 2)) / score

    else:
        print("Даты вне заданных периодов ")
        return 
    

    if DNpen.month == 12:
        if DNpen.year != 31:
            sp_standart_by_year[pension.id][PeriodType(DN=DNpen, DK=date(year, 12, 31))] = summa
        summa = IPK * INSURANCE_PENSION_SCORE[date(DNpen.year+1, 1, 1)] + INSURANCE_PENSION_FIX_AMOUNT[date(DNpen.year+1, 1, 1)]/2
        date_for_period = date(DNpen.year, 12, 31)
        date_index = date(DNpen.year+1, 12, 31)
    else:
        if data.is_payment_transferred:
            if data.is_get_PSD_FSD_last_mounth_payment_trasferred and data.is_get_PSD_FSD_last_year_payment_trasferred:
                if data.is_Not_get_PSD_FSD_now_payment_trasferred:
                    sp_prev = IPK*INSURANCE_PENSION_SCORE[date(DNpen.year-1, 1, 1)] + INSURANCE_PENSION_FIX_AMOUNT[date(DNpen.year-1, 1, 1)]/2
                    sp_standart_by_year[pension.id][PeriodType(DN=date(DNpen.year-1, 12, 31), DK=DNpen)] = sp_prev
                else:
                    isRSD = False
        date_for_period = DNpen
        summa = pension.amount
        date_index = date(DNpen.year, 12, 31)


    while date_index < DKpen:
        if isRSD:
            sp_standart_by_year[pension.id][PeriodType(DN=date_for_period, DK=date_index)] = summa
        else:
            sp_standart_by_year[pension.id][PeriodType(DN=date_for_period, DK=date_index)] = 0
        
        date_for_period = date_index
        summa = IPK*INSURANCE_PENSION_SCORE[date_index]+INSURANCE_PENSION_FIX_AMOUNT[date_index]
        date_index = date(date_for_period.year+1, 12, 31)
    
    if isRSD:
            sp_standart_by_year[pension.id][PeriodType(DN=date_for_period, DK=DKpen)] = summa
    else:
        sp_standart_by_year[pension.id][PeriodType(DN=date_for_period, DK=DKpen)] = 0

    return sp_standart_by_year



async def pension_social_calculate(data:  JsonQuerySchema, pension: PaymentInterface, sp_standart_by_year) -> PaymentsByYear:

    """ Функция по расчета стандартных выплат по социальной пенсии по годам

    Returns:
        PaymentsByYear: Возвращает словаь с индексом пенсии, которому принадлежит словарь с периодами и соотвествующими стандартными выплатами
    """ 


    DNpen = pension.DN
    DKpen = pension.DK

    year = DNpen.year
    summa = pension.amount
    sp_standart_by_year[pension.id] = {}

    isRSD = True

    # определяем дату индексации
    date_index = date(DNpen.year, 4, 1)

    if DNpen > date_index:
        if data.is_payment_transferred:
            if data.is_get_PSD_FSD_last_mounth_payment_trasferred and data.is_get_PSD_FSD_last_year_payment_trasferred:
                if data.is_Not_get_PSD_FSD_now_payment_trasferred:
                    sp_standart_by_year[pension.id][PeriodType(DN=date(year-1, 12, 1), DK=DNpen)] = summa / SOCIAL_PENSION_INDEX[date_index]
                    date_for_period = DNpen               
                else:
                    isRSD = False # РСД не положено
                    sp_standart_by_year[pension.id][PeriodType(DN=DNpen, DK=date_index)] = 0
    else:
        sp_standart_by_year[pension.id][PeriodType(DN=DNpen, DK=date_index)] = summa
        summa = summa*SOCIAL_PENSION_INDEX[date_index]
        date_for_period = date_index
    

    if date_index == date(2022, 4, 1):
        date_index = date(2022, 6, 1)
    elif date_index == date(2022, 6, 1):
        date_index = date(2023, 4, 1)
    else: date_index = date(date_index.year+1, 4, 1)

    while date_index < DKpen:

        if isRSD:
            sp_standart_by_year[pension.id][PeriodType(DN=date_for_period, DK=date_index)] = summa

        else:
            sp_standart_by_year[pension.id][PeriodType(DN=date_for_period, DK=date_index)] = 0
        
        date_for_period = date_index
        summa = summa*SOCIAL_PENSION_INDEX[date_index]  

        if date_index == date(2022, 4, 1):
            date_index = date(2022, 6, 1)
        elif date_index == date(2022, 6, 1):
            date_index = date(2023, 4, 1)
        else: date_index = date(date_index.year+1, date_index.month, date_index.day) 

    if isRSD:
        sp_standart_by_year[pension.id][PeriodType(DN=date_for_period, DK=DKpen)] = summa
    else:
        sp_standart_by_year[pension.id][PeriodType(DN=date_for_period, DK=DKpen)] = 0
    
    return sp_standart_by_year



async def pension_departmental_calculate(pension: PaymentInterface, sp_standart_by_year) -> PaymentsByYear:

    """ Функция по расчета стандартных выплат по ведомственной пенсии по годам

    Returns:
        PaymentsByYear: Возвращает словаь с индексом пенсии, которому принадлежит словарь с периодами и соотвествующими стандартными выплатами
    """ 
    DNpen = pension.DN
    DKpen = pension.DK

    if (pension.is_recalculation and pension.recalculation != None):
        n = len(pension.recalculation)
        for i in range(n):
            date_rec = pension.recalculation[i].date
            date_rec_prev = pension.recalculation[i-1].date
            amount_rec_prev = pension.recalculation[i-1].amount
            if DNpen < date_rec <= DKpen:
                if i == 0:
                    sp_standart_by_year[pension.id][PeriodType(DN=DNpen, DK=date_rec)] = pension.amount
                elif i == n:
                    sp_standart_by_year[pension.id][PeriodType(DN=date_rec_prev, DK=DKpen)] = amount_rec_prev
                else:
                    sp_standart_by_year[pension.id][PeriodType(DN=date_rec_prev, DK=date_rec)] = amount_rec_prev
    else:
        sp_standart_by_year[pension.id][PeriodType(DN=DNpen, DK=DKpen)] = pension.amount
    
    return sp_standart_by_year





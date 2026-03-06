from src.constants.payment_const import SOCIAL_PENSION_INDEX, INSURANCE_PENSION_SCORE, INSURANCE_PENSION_FIX_AMOUNT
from datetime import date
from typing import  Dict

from src.utils.payments.types.paymentType import PaymentsByYear
from src.schemas.json_query_schema import (
    JsonQuerySchema, PaymentInterface
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
            sp_standart_by_year = await pension_insurance_SPK_calculate(data, pension, sp_standart_by_year)
        elif pension.categoria == "social_SPK" or pension.categoria == "social_disability":
            pass

    return sp_standart_by_year
    


async def pension_insurance_SPK_calculate(data: JsonQuerySchema, pension: PaymentInterface, sp_standart_by_year) -> Dict[int, float]:

    """ Функция по расчета стандартных выплат по страховой пенсии по годам

    Returns:
        PaymentsByYear: Возвращает словаь с индексом пенсии, которому принадлежит словарь с годами и соотвествующими стандартными выплатами
    """ 

    DNpen = pension.DN
    year = DNpen.year
    sp = pension.amount

    score_fix = get_score_fix_amount_insurance(DNpen)
    score = score_fix['score']
    fix_amount = score_fix['fix_amount'] / 2

    sp_standart_by_year[pension.id] = {}

    if (score != 0 and fix_amount != 0):
        IPK = (pension.amount - (fix_amount / 2)) / score

    else:
        print("Даты вне заданных периодов ")
        return 

    if data.is_payment_transferred:
        if data.is_get_PSD_FSD_last_mounth_payment_trasferred and data.is_get_PSD_FSD_last_year_payment_trasferred:
            if data.is_Not_get_PSD_FSD_now_payment_trasferred:
                if DNpen.month != 12:
                    sp = IPK*INSURANCE_PENSION_SCORE[date(year-1, 1, 1)] + (INSURANCE_PENSION_FIX_AMOUNT[date(year-1, 1, 1)] / 2)
            else: sp_standart_by_year[pension.id][pension.DN.year] = 0

    
    current_year = date.today().year

    while year < current_year:
        sp_standart_by_year[pension.id][year] = sp
        year+=1
        sp = IPK*INSURANCE_PENSION_SCORE[date(year, 1, 1)] + (INSURANCE_PENSION_FIX_AMOUNT[date(year, 1, 1)] / 2)

    sp_standart_by_year[pension.id][year] = sp

    return sp_standart_by_year



async def pension_social_calculate(data:  JsonQuerySchema, pension: PaymentInterface, sp_standart_by_year) -> Dict[int, float]:

    """ Функция по расчета стандартных выплат по социальной пенсии по годам

    Returns:
        PaymentsByYear: Возвращает словаь с индексом пенсии, которому принадлежит словарь с годами и соотвествующими стандартными выплатами
    """ 


    DNpen = pension.DN
    # score_fix = get_score_fix_amount_insurance(DNpen)
    # score = score_fix['score']
    # fix_amount = score_fix['fix_amount'] / 2

    # year = DNpen.year

    sp_standart_by_year[pension.id] = {}

    # if (score != 0 and fix_amount != 0):
    #     IPK = (pension.amount - (fix_amount / 2)) / score

    # else:
    #     print("Даты вне заданных периодов ")
    #     return 

    # определяем дату индексации
    date_index = date(DNpen.year+1, 4, 1)

    if DNpen > date_index:
        pass
    else:
        pass
        
    
    
    return sp_standart_by_year





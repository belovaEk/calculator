from src.constants.payment_const import INSURANCE_PENSION_SCORE, INSURANCE_PENSION_FIX_AMOUNT
from datetime import date

from src.utils.payments.types.paymentType import PaymentsByYear
from src.schemas.json_query_schema import (
    JsonQuerySchema,
)

async def pension_insurance_SPK_amount(data: JsonQuerySchema) -> PaymentsByYear:

    """ Функция по расчета стандартных выплат по страховой пенсии по годам

    Returns:
        PaymentsByYear: Возвращает словаь с индексом пенсии, которому принадлежит словарь с годами и соотвествующими стандартными выплатами
    """    
    pensions = [p for p in data.payments if p.type == 'pension']
    insurance_pension_by_year: PaymentsByYear = {}

    for pension in pensions:

        DNpen = pension.DN

        score_fix = get_score_fix_amount(DNpen)
        score = score_fix['score']
        fix_amount = score_fix['fix_amount'] / 2

        year = DNpen.year

        insurance_pension_by_year[pension.id] = {}

        if (score != 0 and fix_amount != 0):
            IPK = (pension.amount - (fix_amount / 2)) / score

        else:
            print("Даты вне заданных периодов ")
            return 
        
        sp = pension.amount

        current_year = date.today().year

        while year < current_year:
            insurance_pension_by_year[pension.id][year] = sp
            year+=1
            sp = IPK*INSURANCE_PENSION_SCORE[date(year, 1, 1)] + (INSURANCE_PENSION_FIX_AMOUNT[date(year, 1, 1)] / 2)

        insurance_pension_by_year[pension.id][year] = sp
    
    return insurance_pension_by_year


def get_score_fix_amount(DNpen: date):
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
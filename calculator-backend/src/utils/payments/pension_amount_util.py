from constants.payment_const import INSURANCE_PENSION_SCORE, INSURANCE_PENSION_FIX_AMOUNT
from datetime import date

from src.utils.payments.types.paymentType import PaymentsByYear
from src.schemas.json_query_schema import (
    JsonQuerySchema,
)

async def pension_insurance_SPK_amount(data: JsonQuerySchema) -> PaymentsByYear:

    pensions = [p for p in data.payments if p.type == 'pension']
    insurance_pension_by_year: PaymentsByYear = {}

    for pension in pensions:

        DNpen = pension.DN
        score = get_score_fix_amount['score']
        fix_amount = get_score_fix_amount['fix_amount']

        year = DNpen.year

        insurance_pension_by_year[pension.id] = {}
        IPK = (pension.amount - fix_amount) / score

        sp = pension.amount

        current_year = date.today().year
        while year < current_year:
            insurance_pension_by_year[pension.id][year] = sp
            year+=1
            sp = IPK*INSURANCE_PENSION_SCORE[date(year, 01, 01)]+INSURANCE_PENSION_FIX_AMOUNT[date(year, 01, 01)]

        insurance_pension_by_year[pension.id][year] = sp
    
    return {
        'sp_standart': insurance_pension_by_year
    }



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
# from typing import List, Dict, TypeAlias
from src.utils.payments.constants.payment_const import INSURANCE_PENSION_SCORE, INSURANCE_PENSION_FIX_AMOUNT


from src.utils.payments.types.paymentType import AmountByYear, PaymentsByYear

from dateutil.relativedelta import relativedelta
from src.schemas.json_query_schema import (
    JsonQuerySchema,
    PeriodType,
)

async def pension_insurance_SPK_amount(data: JsonQuerySchema) -> PaymentsByYear:

    pensions = [p for p in data.payments if p.type == 'pension']
    insurance_pension_by_year: PaymentsByYear = {}

    for pension in pensions:

        current_pension_amount = insurance_pension_by_year[pension.id]
        pass




    # year = DN.year
    # IPK = (sp[year] -fix_amount[year])/ipk[year]
    # while year != current_year:
    #     year: IPK
    #     year +=1
    #     sp[ year +=1] = IPK*ipk[ year +=1]+ fix_amount[year+1]

    # year: IPK
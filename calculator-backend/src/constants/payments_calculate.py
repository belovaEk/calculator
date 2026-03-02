from src.utils.payments.pension_amount_util import pension_insurance_SPK_amount
from src.utils.payments.types.paymentType import PaymentsByYear
from src.schemas.json_query_schema import (
    JsonQuerySchema,
)

SP_STANDART: PaymentsByYear = {}

async def calculate_payments_standart(data: JsonQuerySchema):
    SP_STANDART = await pension_insurance_SPK_amount(data)
    return SP_STANDART


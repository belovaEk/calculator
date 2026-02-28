from pydantic import BaseModel
from datetime import date
from typing import List, Optional, Literal


class RegistrationPeriod(BaseModel):
    DN: date
    DK: date


class SuspensionPeriodType(BaseModel):
    id: int
    DN: date
    DK: date


PaymentTypeRaw = Literal['pension', 'edv', 'egdv', 'housin', 'custom']
PensionCategoryRaw = Literal['insurance_SPK', 'social_SPK', 'social_disability']


class PaymentInterface(BaseModel):
    id: int
    type: PaymentTypeRaw
    categoria: PensionCategoryRaw | str = ''
    DN: date
    DK: date
    paymentAmount: float  # Rubles
    is_Moscow: bool
    is_suspension: bool
    suspension: Optional[List[SuspensionPeriodType]] = None



class JsonQuerySchema(BaseModel):
    is_adult: bool
    date_of_birth: date
    document_on_full_time_OOP_education: bool
    type_of_social_payment: str
    is_there_a_registration_in_moscow: bool
    is_there_a_registration_in_moscow_of_the_breadwinner: bool
    is_there_a_registration_in_moscow_of_the_legal_representative: bool
    periods_of_registration_in_moscow: List[RegistrationPeriod]
    periods_of_registration_in_moscow_of_the_breadwinner: List[RegistrationPeriod]
    periods_of_registration_in_moscow_of_the_legal_representative: List[RegistrationPeriod]
    date_of_death_of_the_breadwinner: str
    there_is_a_breadwinner: bool

    is_payment_transferred: Optional[bool] = None
    is_get_PSD_FSD_last_mounth_payment_trasferred: Optional[bool] = None
    is_Not_get_PSD_FSD_now_payment_trasferred: Optional[bool] = None
    payments: Optional[List[PaymentInterface]] = None

from pydantic import BaseModel
from datetime import date
from typing import List

class RegistrationPeriod(BaseModel):
    DN: date
    DK: date

class JsonQuerySchema(BaseModel):
    is_adult: bool
    date_of_birth: int
    document_on_full_time_OOP_education: bool
    date_of_the_initial_appointment_of_the_SPV_is_137_or_143: date
    type_of_social_payment: str
    is_there_a_registration_in_moscow: bool
    is_there_a_registration_in_moscow_of_the_breadwinner: bool
    is_there_a_registration_in_moscow_of_the_legal_representative: bool
    periods_of_registration_in_moscow: List[RegistrationPeriod]
    periods_of_registration_in_moscow_of_the_breadwinner: List[RegistrationPeriod]
    periods_of_registration_in_moscow_of_the_legal_representative: List[RegistrationPeriod]
    date_of_appointment_of_the_spv: str
    date_of_death_of_the_breadwinner: str
    there_is_a_breadwinner: bool

from pydantic import BaseModel
from datetime import date
from typing import List, Optional, Literal
from dateutil.relativedelta import relativedelta


class RegistrationPeriod(BaseModel):
    DN: date
    DK: date


class SuspensionPeriodType(BaseModel):
    id: int
    DN: date
    DK: date


PaymentTypeRaw = Literal["pension", "edv", "egdv", "housin", "custom"]
PensionCategoryRaw = Literal["insurance_SPK", "social_SPK", "social_disability"]


class PaymentInterface(BaseModel):
    id: int
    type: PaymentTypeRaw
    categoria: PensionCategoryRaw | str = ""
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
    periods_reg_moscow: List[RegistrationPeriod]
    periods_reg_representative_moscow: List[RegistrationPeriod]
    periods_reg_breadwinner_moscow: List[RegistrationPeriod]
    date_of_death_of_the_breadwinner: date
    there_is_a_breadwinner: bool

    is_payment_transferred: Optional[bool] = None
    is_get_PSD_FSD_last_mounth_payment_trasferred: Optional[bool] = None
    is_Not_get_PSD_FSD_now_payment_trasferred: Optional[bool] = None
    payments: Optional[List[PaymentInterface]] = None



class RegistrationPeriod(BaseModel):
    DN: date
    DK: date

class PeriodDuration(BaseModel):
    years: int = 0
    months: int = 0
    days: int = 0
    
    def __add__(self, other: 'PeriodDuration') -> 'PeriodDuration':
        return PeriodDuration(
            years=self.years + other.years,
            months=self.months + other.months,
            days=self.days + other.days
        )
    
    def __sub__(self, other: 'PeriodDuration') -> 'PeriodDuration':
        return PeriodDuration(
            years=self.years - other.years,
            months=self.months - other.months,
            days=self.days - other.days
        )
    
    def to_relativedelta(self) -> relativedelta:
        return relativedelta(years=self.years, months=self.months, days=self.days)
    
    @classmethod
    def from_relativedelta(cls, rd: relativedelta) -> 'PeriodDuration':
        return cls(
            years=rd.years or 0,
            months=rd.months or 0,
            days=rd.days or 0
        )
    
    def __str__(self):
        parts = []
        if self.years:
            parts.append(f"{self.years} г.")
        if self.months:
            parts.append(f"{self.months} мес.")
        if self.days:
            parts.append(f"{self.days} дн.")
        return " ".join(parts) if parts else "0 дн."
    
    class Config:
        arbitrary_types_allowed = True

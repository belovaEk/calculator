from pydantic import BaseModel
from datetime import date
from typing import List, Optional, Literal
from dateutil.relativedelta import relativedelta


class PeriodType(BaseModel):
    DN: date
    DK: date
    
class PeriodWithIdType(PeriodType):
    id: int


class OrderType(BaseModel):
    id: int
    date: date

PaymentTypeRaw = Literal["pension", "edv", "egdv", "housin", "custom"]
PensionCategoryRaw = Literal["insurance_SPK", "social_SPK", "social_disability", "departmental"]

PensionCategoryAdultRaw = Literal["insurance", "social", "departmental", "gosudarstvennaya", "other", "monthPay"]
PersonCategoryRaw = Literal['reabilitirovan', 'truzhennik', 'war_child','labor_veteran','labor_veteran_55_60']




class RecalculationData(BaseModel):
    date: date
    amount: float


class PaymentInterface(BaseModel):
    id: int
    type: PaymentTypeRaw
    categoria: PensionCategoryRaw | PensionCategoryAdultRaw | PersonCategoryRaw
    DN: date 
    DK: date 
    amount: float  
    is_Moscow: bool

    is_recalculation:  Optional[bool] = None
    recalculation: Optional[List[RecalculationData]] = None

    is_payment_transferred: bool
    is_get_PSD_FSD_last_mounth_payment_trasferred: Optional[bool] = False
    is_get_PSD_FSD_last_year_payment_trasferred: Optional[bool] = False
    is_Not_get_PSD_FSD_now_payment_trasferred: Optional[bool] = False

    is_fix_amount: Optional[bool] = False
    amount_fix: Optional[float] = None,
    is_recalculation_fix_amount: Optional[bool] = False,
    recalculation_fix_amount: Optional[List[RecalculationData]] = None
    categoria_person: Optional[PersonCategoryRaw] = None

    # invalid_categoria: Optional[int] = None
    # num_dependents: Optional[int] = None


    

class JsonQuerySchema(BaseModel):
    is_adult: bool = None
    date_of_birth: date = None
    document_on_full_time_OOP_education: Optional[bool] = None
    is_there_a_registration_in_moscow: bool
    is_there_a_registration_in_moscow_of_the_breadwinner: bool
    is_there_a_registration_in_moscow_of_the_legal_representative: bool
    periods_reg_moscow: Optional[List[PeriodType]] = None
    periods_reg_representative_moscow: Optional[List[PeriodType]] = None
    periods_reg_breadwinner_moscow: Optional[List[PeriodType]] = None
    date_of_death_of_the_breadwinner: Optional[date] = None
    there_is_a_breadwinner: bool

    payments: Optional[List[PaymentInterface]] = None
    
    periods_suspension: Optional[List[PeriodWithIdType]] = None
    periods_inpatient: Optional[List[PeriodWithIdType]] = None
    periods_employment: Optional[List[PeriodWithIdType]] = None
    is_order: Optional[bool] = None
    orders_date: Optional[List[OrderType]] = None
    change_last_date: Optional[date] = None

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
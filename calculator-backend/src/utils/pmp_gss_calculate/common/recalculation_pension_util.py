from src.schemas.json_query_schema import PeriodType, PeriodType, PaymentInterface
from typing import List, Dict, TypeAlias
GssPmpPensionType: TypeAlias = Dict[int, List[PeriodType]]


def recalculation_payment (pensions: List[PaymentInterface], n: int, periods: List[PeriodType]):

    new_periods: GssPmpPensionType = {}
    for i in range(n):

        if not pensions[i].is_Moscow:
            continue

        DNpen = pensions[i].DN
        DKpen = pensions[i].DK

        new_periods[i] = []

        for period in periods:
                
            DN_gss_pmp = period.DN
            DK_gss_pmp = period.DK

            # Если пенсия полностью внутри ПМП и ГСС
            if DN_gss_pmp <= DNpen < DKpen <= DK_gss_pmp:
                new_periods[i].append(PeriodType(DN=DNpen, DK=DKpen))
           
            # Если начало пенсии внутри ГСС или ПМП
            elif DN_gss_pmp <= DNpen < DK_gss_pmp:
                new_periods[i].append(PeriodType(DN=DNpen, DK=DK_gss_pmp))
                        
            # Если конец пенсии внутри ГСС или ПМП 
            elif DN_gss_pmp < DKpen <= DK_gss_pmp:
                new_periods[i].append(PeriodType(DN=DN_gss_pmp, DK=DKpen))

            # Если периоды ГСС или ПМП внутри пенсии
            elif DNpen < DN_gss_pmp < DK_gss_pmp <DKpen:
                new_periods[i].append(PeriodType(DN=DN_gss_pmp, DK=DK_gss_pmp))


    return new_periods
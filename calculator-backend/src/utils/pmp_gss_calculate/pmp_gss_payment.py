from src.schemas.json_query_schema import JsonQuerySchema, PeriodType, PeriodType, PeriodWithIdType, PaymentInterface
from typing import List, Dict, TypeAlias

GssPmpPensionType: TypeAlias = Dict[int, List[PeriodType]]

async def pmp_gss_pension (data: JsonQuerySchema, pmp_periods: List[PeriodType], gss_periods: List[PeriodType]):
    
    pensions = [p for p in data.payments if p.type == 'pension']
    n = len(pensions)

    if n > 1:
        new_pmp_periods = recalculation(pensions=pensions, n=n, periods=pmp_periods)
        new_gss_periods = recalculation(pensions=pensions, n=n, periods=gss_periods) 

        return {
            'pmp_periods': new_pmp_periods,
            'gss_periods': new_gss_periods
        }
    else:
        return {
            'pmp_periods': pmp_periods,
            'gss_periods': gss_periods
        }
    


def recalculation (pensions: List[PaymentInterface], n: int, periods: List[PeriodType]):
    new_periods: GssPmpPensionType = {}
    for i in range( n - 1):

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


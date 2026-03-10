from src.utils.pmp_gss_calculate.type import GssPmpIndexType
from src.utils.payments.pension_amount_util import calculate_sp_standart
from src.schemas.json_query_schema import JsonQuerySchema
from src.utils.payments.types.paymentType import (
    PaymentsByPeriods,
    PeriodAmount,
    PeriodAmountWithSP,
)
from typing import List, Dict
from dateutil.relativedelta import relativedelta


async def alt_pmp_gss_payment_amount(
    pmp_periods: Dict[int, List[PeriodAmount]],
    gss_periods: Dict[int, List[PeriodAmount]],
    data: JsonQuerySchema,
) -> Dict[str, Dict[int, List[PeriodAmountWithSP]]]:

    try: 
        suspension_periods = data.periods_suspension
        suspension_dks = [p.DK for p in suspension_periods]
    except:
        suspension_periods = []

    sp_standart: PaymentsByPeriods = await calculate_sp_standart(data)

    result_pmp: Dict[int, List[PeriodAmountWithSP]] = {}
    result_gss: Dict[int, List[PeriodAmountWithSP]] = {}

    for l in range(len(pmp_periods)):
        result_pmp.setdefault(l, [])

        # Для ПМП
        for j in range(len(pmp_periods[l])):
            if j == 0:
                if sp_standart[l].is_payment_transferred:
                    if (
                        sp_standart[l].is_get_PSD_FSD_last_mounth_payment_trasferred
                        and sp_standart[l].is_get_PSD_FSD_last_year_payment_trasferred
                    ):
                        if sp_standart[l].is_Not_get_PSD_FSD_now_payment_trasferred:
                            data_poiska_pensii = pmp_periods[l][j].DN - relativedelta(months=1)
                            
                        else:
                            amount = 0
                    else:
                        data_poiska_pensii = pmp_periods[l][j].DN

            # j == 0 = False
            else:
                for k in range(len(suspension_periods)):

                    if k == len(suspension_periods) - 1:
                        data_poiska_pensii = pmp_periods[l][j].DN - relativedelta(months=1)
                        break
                        
                    else: 
                        if pmp_periods[l][j].DN == suspension_periods[k].DK and k >= 1:
                            data_poiska_pensii = suspension_periods[k-1].DK
                            break

            for d in range(len(sp_standart[l].periods)):

                if d == len(sp_standart[l].periods) - 1:
                    sp_amount = 0
                    break

                # Возможно, два нестрогих неравенства здесь в условии ниже:
                if (
                    pmp_periods[l][j].DN
                    <= data_poiska_pensii
                    < pmp_periods[l][j].DK
                ):
                    sp_amount = sp_standart[l].periods[d].amount
                    break

            amount = pmp_periods[l][j].amount - sp_amount
            result_pmp[l].append(
                {
                    "DN": pmp_periods[l][j].DN,
                    "DK": pmp_periods[l][j].DK,
                    "amount": amount,
                    "sp_amount": sp_amount,
                    "pmp_gss_amount": pmp_periods[l][j].amount
                }
            )

        # Для ГСС
        result_gss.setdefault(l, [])
        for j in range(len(pmp_periods[l])):
            data_poiska_pensii = pmp_periods[l][j].DN - relativedelta(months=1)

            for d in range(len(sp_standart[l].periods)):

                if d == len(sp_standart[l].periods) - 1:
                    sp_amount = 0
                    break

                # Возможно, два нестрогих неравенства здесь в условии ниже:
                if (
                    gss_periods[l][j].DN
                    <= data_poiska_pensii
                    < gss_periods[l][j].DK
                ):
                    sp_amount = sp_standart[l].periods[d].amount
                    break

            amount = gss_periods[l][j].amount - sp_amount
            result_gss[l].append(
                {
                    "DN": pmp_periods[l][j].DN,
                    "DK": pmp_periods[l][j].DK,
                    "amount": amount,
                    "sp_amount": sp_amount,
                    "pmp_gss_amount": pmp_periods[l][j].amount
                }
            )
                    
                
        


    return {"pmp_periods": result_pmp, "gss_periods": result_gss}

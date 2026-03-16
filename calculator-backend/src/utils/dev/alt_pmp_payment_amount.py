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


async def alt_pmp_payment_amount(
    pmp_periods: Dict[int, List[PeriodAmount]],
    data: JsonQuerySchema,
) -> Dict[int, List[PeriodAmountWithSP]]:

    if not (data.periods_suspension):
        suspension_periods = []
    else:
        suspension_periods = data.periods_suspension

    sp_standart: PaymentsByPeriods = await calculate_sp_standart(data)

    result_pmp: Dict[int, List[PeriodAmountWithSP]] = {}

    for l in range(len(pmp_periods)):
        result_pmp.setdefault(l, [])

        # Для ПМП
        for j in range(len(pmp_periods[l])):
            sp_amount = 0  # Инициализация по умолчанию
            # По блок-схеме для j==0 базовая дата поиска = дата начала периода,
            # для остальных периодов (j>0) — дата начала периода минус 1 месяц (если не найдено возобновление).
            if j == 0:
                data_poiska_pensii = pmp_periods[l][j].DN
                if sp_standart[l].is_payment_transferred:
                    if (
                        sp_standart[l].is_get_PSD_FSD_last_mounth_payment_trasferred
                        and sp_standart[l].is_get_PSD_FSD_last_year_payment_trasferred
                    ):
                        if sp_standart[l].is_Not_get_PSD_FSD_now_payment_trasferred:
                            data_poiska_pensii = pmp_periods[l][j].DN - relativedelta(
                                months=1
                            )
                        else:
                            # Ветка "РСД до ПМП = 0": создаём запись с amount = 0 и переходим к следующему периоду
                            result_pmp[l].append(
                                PeriodAmountWithSP(
                                    DN=pmp_periods[l][j].DN,
                                    DK=pmp_periods[l][j].DK,
                                    amount=0.0,
                                    sp_amount=0.0,
                                    pmp_gss_amount=round(pmp_periods[l][j].amount, 2),
                                )
                            )
                            continue
                    else:
                        data_poiska_pensii = pmp_periods[l][j].DN

            # j != 0
            else:
                data_poiska_pensii = pmp_periods[l][j].DN - relativedelta(months=1)
                for k in range(len(suspension_periods)):
                    if pmp_periods[l][j].DN == suspension_periods[k].DK and k >= 1:
                        # дата поиска = дата приостановки (k-1) - 1 месяц
                        data_poiska_pensii = suspension_periods[k-1].DK - relativedelta(months=1)
                        break

            # Поиск подходящего sp_standart периода
            for period in sp_standart[l].periods:
                if period.DN <= data_poiska_pensii < period.DK:
                    sp_amount = round(period.amount, 2)
                    break

            amount = round(pmp_periods[l][j].amount - sp_amount, 2)
            
            if j != 0 and amount > pmp_periods[l][j - 1].amount:
                result_pmp[l].append(
                    PeriodAmountWithSP(
                        DN=pmp_periods[l][j].DN,
                        DK=pmp_periods[l][j].DK,
                        amount=amount,
                        sp_amount=sp_amount,
                        pmp_gss_amount=round(pmp_periods[l][j - 1].amount, 2),
                    )
                )
            else:
                result_pmp[l].append(
                    PeriodAmountWithSP(
                        DN=pmp_periods[l][j].DN,
                        DK=pmp_periods[l][j].DK,
                        amount=amount,
                        sp_amount=sp_amount,
                        pmp_gss_amount=round(pmp_periods[l][j].amount, 2),
                    )
                )

    return {
        "pmp_periods": result_pmp
    }
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


async def pmp_gss_payment_amount_adult(
    pmp_periods: Dict[int, List[PeriodAmount]],
    gss_periods: Dict[int, List[PeriodAmount]],
    omo_pmp: dict,
    omo_gss: dict,
    data: JsonQuerySchema
) -> Dict[str, Dict[int, List[PeriodAmountWithSP]]]:

    if data.periods_suspension:
        suspension_periods = data.periods_suspension
    else:
        suspension_periods = []

    result_pmp: Dict[int, List[PeriodAmountWithSP]] = {}
    result_gss: Dict[int, List[PeriodAmountWithSP]] = {}

    for l in range(len(pmp_periods)):
        result_pmp.setdefault(l, [])

        omo_pmp_l = omo_pmp.get(l)

        for j in range(len(pmp_periods[l])):
            DN = pmp_periods[l][j].DN
            DK = pmp_periods[l][j].DK
            pmp_amount = pmp_periods[l][j].amount

            # Определяем дату поиска для первого подпериода
            if j == 0:
                data_poiska_pensii = DN
                if omo_pmp_l and omo_pmp_l.is_payment_transferred:
                    if (
                        omo_pmp_l.is_get_PSD_FSD_last_mounth_payment_trasferred
                        and omo_pmp_l.is_get_PSD_FSD_last_year_payment_trasferred
                    ):
                        if omo_pmp_l.is_Not_get_PSD_FSD_now_payment_trasferred:
                            data_poiska_pensii = DN - relativedelta(months=1)
                        else:
                            # Ветка "РСД до ПМП = 0"
                            result_pmp[l].append(
                                PeriodAmountWithSP(
                                    DN=DN,
                                    DK=DK,
                                    amount=0.0,
                                    sp_amount=0.0,
                                    pmp_gss_amount=round(pmp_amount, 2),
                                )
                            )
                            continue
            else:
                # Если пенсионный период начинается ровно в DN (смена констант на границе года),
                # используем DN напрямую — константы актуальны с этой даты, а не с прошлого месяца
                if omo_pmp_l and any(period.DN == DN for period in omo_pmp_l.periods):
                    data_poiska_pensii = DN
                else:
                    data_poiska_pensii = DN - relativedelta(months=1)
                for k in range(len(suspension_periods)):
                    if DN == suspension_periods[k].DK and k >= 1:
                        data_poiska_pensii = suspension_periods[k - 1].DK - relativedelta(months=1)
                        break

            # Брейкпоинты из пенсионных периодов, которые попадают строго внутрь (DN, DK)
            pension_breakpoints = []
            if omo_pmp_l:
                pension_breakpoints = sorted({
                    d
                    for period in omo_pmp_l.periods
                    for d in (period.DN, period.DK)
                    if DN < d < DK
                })

            # Разбиваем ПМП-период на подпериоды по брейкпоинтам пенсий
            sub_starts = [DN] + pension_breakpoints
            sub_ends = pension_breakpoints + [DK]

            prev_pmp_amount = pmp_periods[l][j - 1].amount if j > 0 else None

            for sub_idx, (sub_DN, sub_DK) in enumerate(zip(sub_starts, sub_ends)):
                # Первый подпериод: исходная дата поиска (с учётом j/suspension логики)
                # Последующие подпериоды (разрывы по пенсиям): дата начала подпериода напрямую
                lookup_date = data_poiska_pensii if sub_idx == 0 else sub_DN

                sp_amount = 0
                if omo_pmp_l:
                    for period in omo_pmp_l.periods:
                        if period.DN <= lookup_date < period.DK:
                            sp_amount = round(period.amount, 2)
                            break

                unclamped = pmp_amount - sp_amount
                amount = round(max(0.0, unclamped), 2)

                # pmp_gss_amount: для первого подпериода нового года (j>0) применяем оригинальную логику
                if sub_idx == 0 and j != 0 and unclamped > prev_pmp_amount:
                    pmp_gss_amount = round(prev_pmp_amount, 2)
                else:
                    pmp_gss_amount = round(pmp_amount, 2)

                result_pmp[l].append(
                    PeriodAmountWithSP(
                        DN=sub_DN,
                        DK=sub_DK,
                        amount=amount,
                        sp_amount=sp_amount,
                        pmp_gss_amount=pmp_gss_amount,
                    )
                )

        # Для ГСС
        result_gss.setdefault(l, [])
        omo_gss_l = omo_gss.get(l)

        for j in range(len(gss_periods[l])):
            sp_amount = 0
            data_poiska_pensii = gss_periods[l][j].DN
            if omo_gss_l:
                for period in omo_gss_l.periods:
                    if period.DN <= data_poiska_pensii < period.DK:
                        sp_amount = round(period.amount, 2)
                        break

            unclamped = gss_periods[l][j].amount - sp_amount
            amount = round(max(0.0, unclamped), 2)

            if j != 0 and unclamped > gss_periods[l][j - 1].amount:
                result_gss[l].append(
                    PeriodAmountWithSP(
                        DN=gss_periods[l][j].DN,
                        DK=gss_periods[l][j].DK,
                        amount=amount,
                        sp_amount=sp_amount,
                        pmp_gss_amount=round(gss_periods[l][j - 1].amount, 2),
                    )
                )
            else:
                result_gss[l].append(
                    PeriodAmountWithSP(
                        DN=gss_periods[l][j].DN,
                        DK=gss_periods[l][j].DK,
                        amount=amount,
                        sp_amount=sp_amount,
                        pmp_gss_amount=round(gss_periods[l][j].amount, 2),
                    )
                )

    return {"pmp_periods": result_pmp, "gss_periods": result_gss}
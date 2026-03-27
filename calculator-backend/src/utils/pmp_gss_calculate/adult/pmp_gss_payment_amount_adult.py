from datetime import date
from typing import List, Dict, Set, Tuple, Optional
from collections import defaultdict
from dateutil.relativedelta import relativedelta

from src.utils.pmp_gss_calculate.type import GssPmpIndexType
from src.utils.payments.pension_amount_util import calculate_sp_standart
from src.schemas.json_query_schema import JsonQuerySchema
from src.utils.payments.types.paymentType import (
    PaymentsByPeriods,
    PeriodAmount,
    PeriodAmountWithSP,
)
from src.utils.pmp_gss_calculate.adult.payment_breakpoints_util import (
    get_payment_breakpoints_from_schema,
    split_period_by_breakpoints
)


async def pmp_gss_payment_amount_adult(
    pmp_periods: Dict[int, List[PeriodAmount]],
    gss_periods: Dict[int, List[PeriodAmount]],
    omo_pmp: dict,
    omo_gss: dict,
    data: JsonQuerySchema
) -> Dict[str, Dict[int, List[PeriodAmountWithSP]]]:

    # Отладка: проверяем, есть ли housin в data.payments
    print(f"\n=== PMP_GSS_PAYMENT_AMOUNT_ADULT ===")
    print(f"data.payments count: {len(data.payments) if data.payments else 0}")
    if data.payments:
        housin_count = sum(1 for p in data.payments if p.type == "housin")
        print(f"Housin in data.payments: {housin_count}")
        for p in data.payments:
            if p.type == "housin":
                print(f"  Housin: {p.DN.strftime('%d.%m.%Y')} - {p.DK.strftime('%d.%m.%Y')}, amount: {p.amount}")

    if data.periods_suspension:
        suspension_periods = data.periods_suspension
    else:
        suspension_periods = []
    
    if not (data.periods_inpatient):
        periods_inpatient = []
    else:
        periods_inpatient = data.periods_inpatient

    if not (data.periods_employment):
        periods_employment = []
    else:
        periods_employment = data.periods_employment

    result_pmp: Dict[int, List[PeriodAmountWithSP]] = {}
    result_gss: Dict[int, List[PeriodAmountWithSP]] = {}

    # Получаем список всех выплат из данных
    all_payments = data.payments if data.payments else []
    
    for l in range(len(pmp_periods)):
        result_pmp.setdefault(l, [])

        omo_pmp_l = omo_pmp.get(l)

        for j in range(len(pmp_periods[l])):
            DN = pmp_periods[l][j].DN
            DK = pmp_periods[l][j].DK
            pmp_amount = pmp_periods[l][j].amount

            print(f"\n=== PERIOD {l},{j} ===")
            print(f"Period: {DN.strftime('%d.%m.%Y')} - {DK.strftime('%d.%m.%Y')}")

            # Получаем брейкпоинты на основе всех выплат
            breakpoints = get_payment_breakpoints_from_schema(
                data=data,
                start_date=DN,
                end_date=DK
            )

            print(f"Breakpoints: {[bp.strftime('%d.%m.%Y') for bp in breakpoints]}")
            
            # Разбиваем период на подпериоды по брейкпоинтам
            subperiods = split_period_by_breakpoints(DN, DK, breakpoints)
            
            # Определяем дату поиска для первого подпериода
            if j == 0:
                data_poiska_pensii = DN
                if len(gss_periods[l]) >= 1 and pmp_periods[l][j].DN < gss_periods[l][0].DN:
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
                data_poiska_pensii = DN - relativedelta(months=1)
                for k in range(len(suspension_periods)):
                    if DN == suspension_periods[k].DK and k >= 1:
                        data_poiska_pensii = date(data.periods_suspension[k].DN.year - 1, 12, 1)
                        break
                for k in range(len(periods_inpatient)):
                    if DN == (periods_inpatient[k].DN+ relativedelta(months=1)).replace(day=1):
                        data_poiska_pensii = date(data.periods_inpatient[k].DN.year - 1, 12, 1)
                        break
                for k in range(len(periods_employment)):
                    if DN == (periods_employment[k].DK+ relativedelta(months=1)).replace(day=1):
                        data_poiska_pensii = date(data.periods_employment[k].DN.year - 1, 12, 1)
                        break

            # Обрабатываем каждый подпериод
            for sub_idx, (sub_DN, sub_DK) in enumerate(subperiods):
                # Первый подпериод: исходная дата поиска (с учётом j/suspension логики)
                # Последующие подпериоды: дата начала подпериода напрямую
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
                if sub_idx == 0 and j != 0 and unclamped < pmp_periods[l][j - 1].amount:
                    pmp_gss_amount = round(pmp_periods[l][j - 1].amount, 2)
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

            if j != 0 and unclamped < gss_periods[l][j - 1].amount:
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
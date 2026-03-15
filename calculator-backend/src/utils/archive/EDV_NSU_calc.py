from datetime import date
from typing import Dict, List

from src.schemas.json_query_schema import JsonQuerySchema, PaymentInterface
from src.utils.payments.types.paymentType import PeriodAmount


EDV_INDEX_COEFFICIENTS: Dict[date, float] = {
    date(2017, 2, 1): 1.054,
    date(2018, 2, 1): 1.025,
    date(2019, 2, 1): 1.043,
    date(2020, 2, 1): 1.030,
    date(2021, 2, 1): 1.063,
    date(2022, 2, 1): 1.086,
    date(2023, 2, 1): 1.122,
    date(2024, 2, 1): 1.075,
    date(2025, 2, 1): 1.095,
    date(2026, 2, 1): 1.026,
}


def _find_k_ind_year(
    d_j: date,
    index_dates: List[date],
    coefficients: Dict[date, float],
) -> float:
    n = len(index_dates)

    i = 0
    while True:
        if i == n:
            k_ind_god = 0.0
            return k_ind_god
        if i == n - 1:
            if index_dates[i] <= d_j:
                k_ind_god = coefficients[index_dates[i]]
            else:
                k_ind_god = 0.0
            return k_ind_god

        if index_dates[i] <= d_j < index_dates[i + 1]:
            k_ind_god = coefficients[index_dates[i]]
            return k_ind_god

        i += 1

async def calculate_edv_nsu(data: JsonQuerySchema) -> Dict[int, List[PeriodAmount]]:
    index_dates: List[date] = sorted(EDV_INDEX_COEFFICIENTS.keys())

    result_edv: Dict[int, List[PeriodAmount]] = {}
    payments = data.payments

    edv_list: List[PaymentInterface] = []
    i = 0
    while True:
        if i == len(payments):
            break
        payment: PaymentInterface = payments[i]
        if payment.type == "pension":
            i += 1
            continue

        if payment.type == "edv":
            edv_list.append(payment)

        i += 1

    edv_list.sort(key=lambda p: p.DN)

    m = len(edv_list)
    j = 0
    while True:
        if j == m:
            break

        current_payment: PaymentInterface = edv_list[j]
        result_edv[current_payment.id] = []

        dn_j: date = current_payment.DN
        dk_j: date = current_payment.DK
        summa_vvedennaya: float = current_payment.amount
        date_ind_j: date = date(dn_j.year, 2, 1)

        if dn_j < date_ind_j:
            d_j: date = dn_j
            date_ind_next: date = date_ind_j
            summa: float = summa_vvedennaya
        else:
            d_j = dn_j
            date_ind_next = date(date_ind_j.year + 1, 2, 1)
            summa = summa_vvedennaya

        while True:
            if not (dk_j > date_ind_next):
                result_edv[current_payment.id].append(
                    PeriodAmount(DN=d_j, DK=dk_j, amount=round(summa, 2))
                )
                break

            else:
                result_edv[current_payment.id].append(
                    PeriodAmount(DN=d_j, DK=date_ind_next, amount=round(summa, 2))
                )

                d_j = date_ind_next

                k_ind_god: float = _find_k_ind_year(
                    d_j=d_j,
                    index_dates=index_dates,
                    coefficients=EDV_INDEX_COEFFICIENTS,
                )

                summa = summa * k_ind_god
                date_ind_next = date(d_j.year + 1, 2, 1)
        j += 1
    return result_edv
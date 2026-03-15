from datetime import date
from typing import Dict, List

from src.schemas.json_query_schema import JsonQuerySchema, PaymentInterface
from src.utils.payments.types.paymentType import PeriodAmount
from src.constants.payments_calculate import EDV_INDEX


def _feb1(year: int) -> date:
    return date(year, 2, 1)


def _get_k_ind(d: date) -> float:
    try:
        k = max(k for k in EDV_INDEX.keys() if k <= d)
    except ValueError:
        return 1.0
    return EDV_INDEX[k]


def _split_edv_period(
    dn: date,
    dk: date,
    amount: float,
) -> List[PeriodAmount]:
    if dn >= dk:
        raise ValueError(f"dn ({dn}) должна быть строго меньше dk ({dk})")

    result: List[PeriodAmount] = []

    d_j = dn
    summa = amount
    feb1_current_year = _feb1(dn.year)
    date_ind_next = feb1_current_year if dn < feb1_current_year else _feb1(dn.year + 1)

    while dk > date_ind_next:
        result.append(PeriodAmount(DN=d_j, DK=date_ind_next, amount=round(summa, 2)))
        d_j = date_ind_next
        summa *= _get_k_ind(d_j)
        date_ind_next = _feb1(d_j.year + 1)

    result.append(PeriodAmount(DN=d_j, DK=dk, amount=round(summa, 2)))
    return result


def calculate_edv_nsu(data: JsonQuerySchema) -> Dict[int, List[PeriodAmount]]:
    result_edv: Dict[int, List[PeriodAmount]] = {}

    edv_payments: List[PaymentInterface] = sorted(
        (p for p in data.payments if p.type == "edv"),
        key=lambda p: p.DN,
    )

    for payment in edv_payments:
        result_edv[payment.id] = _split_edv_period(
            dn=payment.DN,
            dk=payment.DK,
            amount=payment.amount,
        )

    return result_edv


if __name__ == "__main__":
    payment = PaymentInterface(
        id=0,
        type="edv",
        categoria="insurance",
        DN=date(2024, 7, 1),
        DK=date(2025, 7, 1),
        amount=15200,
        is_Moscow=False,
        is_payment_transferred=False,
    )
    payment1 = PaymentInterface(
        id=1,
        type="edv",
        categoria="insurance",
        DN=date(2025, 7, 1),
        DK=date(2026, 3, 1),
        amount=17800,
        is_Moscow=False,
        is_payment_transferred=False,
    )
    data = JsonQuerySchema(
        is_there_a_registration_in_moscow=False,
        is_there_a_registration_in_moscow_of_the_breadwinner=False,
        is_there_a_registration_in_moscow_of_the_legal_representative=False,
        there_is_a_breadwinner=False,
        payments=[payment, payment1],
    )

    result = calculate_edv_nsu(data)

    for pid, periods in result.items():
        print(f"payment id: {pid}")
        for p in periods:
            print("  ", p)
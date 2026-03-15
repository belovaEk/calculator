from datetime import date
from typing import Dict, List

from src.schemas.json_query_schema import JsonQuerySchema, PaymentInterface
from src.utils.payments.types.paymentType import PeriodAmount
from src.constants.payments_calculate import EDK_KIND


def _jan1(year: int) -> date:
    return date(year, 1, 1)


def _get_edk_kind(d: date) -> float:
    try:
        k = max(k for k in EDK_KIND.keys() if k <= d)
    except ValueError:
        return 1.0
    return EDK_KIND[k]


def _split_edk_period(
    dn: date,
    dk: date,
    amount: float,
) -> List[PeriodAmount]:
    if dn >= dk:
        raise ValueError(f"dn ({dn}) должна быть строго меньше dk ({dk})")

    result: List[PeriodAmount] = []

    d_j = dn
    date_ind_next = _jan1(dn.year + 1)
    summa = amount

    while dk > date_ind_next:
        result.append(PeriodAmount(DN=d_j, DK=date_ind_next, amount=round(summa, 2)))
        d_j = date_ind_next
        summa *= _get_edk_kind(d_j)
        date_ind_next = _jan1(d_j.year + 1)

    result.append(PeriodAmount(DN=d_j, DK=dk, amount=round(summa, 2)))
    return result


def calculate_edk(
    data: JsonQuerySchema,
) -> Dict[int, List[PeriodAmount]]:
    result_edk: Dict[int, List[PeriodAmount]] = {}

    edk_payments: List[PaymentInterface] = sorted(
        (p for p in data.payments if p.type == "custom"),
        key=lambda p: p.DN,
    )

    for payment in edk_payments:
        result_edk[payment.id] = _split_edk_period(
            dn=payment.DN,
            dk=payment.DK,
            amount=payment.amount,
        )

    return result_edk


if __name__ == "__main__":
    payment = PaymentInterface(
        id=0,
        type="custom",
        categoria="insurance",
        DN=date(2024, 7, 1),
        DK=date(2025, 7, 1),
        amount=2654,
        is_Moscow=False,
        is_payment_transferred=False,
    )
    payment1 = PaymentInterface(
        id=1,
        type="custom",
        categoria="insurance",
        DN=date(2025, 7, 1),
        DK=date(2026, 3, 1),
        amount=2831.25,
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

    result = calculate_edk(data)
    print(result)

    # for pid, periods in result.items():
    #     print(f"payment id: {pid}")
    #     for p in periods:
    #         print("  ", p)
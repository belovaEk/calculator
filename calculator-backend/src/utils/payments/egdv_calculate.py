from datetime import date
from typing import Dict, List

from src.schemas.json_query_schema import JsonQuerySchema, PaymentInterface
from src.utils.payments.types.paymentType import PeriodAmount
from src.constants.payments_calculate import EGDV_AMOUNTS


def _jan1(year: int) -> date:
    return date(year, 1, 1)


def _get_egdv_amount(d: date, categoria: str) -> float:
    try:
        k = max(k for k in EGDV_AMOUNTS.keys() if k <= d)
    except ValueError:
        raise ValueError(
            f"Дата {d} раньше первой записи в таблице EGDV_AMOUNTS "
            f"({min(EGDV_AMOUNTS.keys())}). Сумма ЕГДВ для этого периода неизвестна."
        )
    return EGDV_AMOUNTS[k][categoria]


def _split_egdv_period(
    dn: date,
    dk: date,
    amount: float,
    categoria: str,
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
        summa = _get_egdv_amount(d_j, categoria)
        date_ind_next = _jan1(d_j.year + 1)

    result.append(PeriodAmount(DN=d_j, DK=dk, amount=round(summa, 2)))
    return result


def calculate_egdv(
    data: JsonQuerySchema,
) -> Dict[int, List[PeriodAmount]]:
    result_egdv: Dict[int, List[PeriodAmount]] = {}

    egdv_payments: List[PaymentInterface] = sorted(
        (p for p in data.payments if p.type == "egdv"),
        key=lambda p: p.DN,
    )

    for payment in egdv_payments:
        result_egdv[payment.id] = _split_egdv_period(
            dn=payment.DN,
            dk=payment.DK,
            amount=payment.amount,
            categoria=payment.categoria_person,
        )

    return result_egdv


if __name__ == "__main__":
    payment = PaymentInterface(
        id=0,
        type="egdv",
        categoria="reabilitirovan",
        DN=date(2024, 7, 1),
        DK=date(2025, 7, 1),
        amount=2654,
        is_Moscow=False,
        is_payment_transferred=False,
    )
    payment1 = PaymentInterface(
        id=1,
        type="egdv",
        categoria="truzhennik",
        DN=date(2025, 7, 1),
        DK=date(2026, 3, 1),
        amount=2100,
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

    result = calculate_egdv(data)

    for pid, periods in result.items():
        print(f"payment id: {pid}")
        for p in periods:
            print("  ", p)
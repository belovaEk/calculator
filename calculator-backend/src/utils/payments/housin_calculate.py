from datetime import date
from typing import Dict, List

from src.schemas.json_query_schema import JsonQuerySchema, PaymentInterface
from src.utils.payments.types.paymentType import PeriodAmount
from src.constants.payments_calculate import HOUSIN_AMOUNTS


def _split_housin_period(
    dn: date,
    dk: date,
) -> List[PeriodAmount]:
    if dn >= dk:
        raise ValueError(f"dn ({dn}) должна быть строго меньше dk ({dk})")

    sorted_dates = sorted(HOUSIN_AMOUNTS.keys())

    applicable = [k for k in sorted_dates if k <= dn]
    if not applicable:
        raise ValueError(
            f"dn ({dn}) раньше первой даты в HOUSIN_AMOUNTS ({sorted_dates[0]}). "
            "Ставка ЖКУ для этого периода неизвестна."
        )
    d = max(applicable)

    result: List[PeriodAmount] = []

    if dn == d:
        current_start = dn
        current_amount = HOUSIN_AMOUNTS[d]

        for boundary in sorted_dates:
            if boundary <= dn:
                continue
            if boundary >= dk:
                break
            result.append(PeriodAmount(DN=current_start, DK=boundary, amount=round(current_amount, 2)))
            current_amount = HOUSIN_AMOUNTS[boundary]
            current_start = boundary

        result.append(PeriodAmount(DN=current_start, DK=dk, amount=round(current_amount, 2)))

    else:
        result.append(PeriodAmount(DN=dn, DK=dk, amount=round(HOUSIN_AMOUNTS[d], 2)))

    return result


def calculate_housin(
    data: JsonQuerySchema,
) -> Dict[int, List[PeriodAmount]]:
    '''
    Возвращает данные формата:
    {
        0: [
            PeriodAmount(DN=datetime.date(2024, 7, 1), DK=datetime.date(2025, 1, 1), amount=2431.07), 
            PeriodAmount(DN=datetime.date(2025, 1, 1), DK=datetime.date(2025, 7, 1), amount=2573.99)
        ], 
        1: [
            PeriodAmount(DN=datetime.date(2025, 9, 1), DK=datetime.date(2026, 3, 1), amount=2831.25)
        ]
    }
    '''
    
    result_housin: Dict[int, List[PeriodAmount]] = {}

    housin_payments: List[PaymentInterface] = sorted(
        (p for p in data.payments if p.type == "housin"),
        key=lambda p: p.DN,
    )

    for payment in housin_payments:
        result_housin[payment.id] = _split_housin_period(
            dn=payment.DN,
            dk=payment.DK,
        )

    return result_housin


if __name__ == "__main__":
    payment = PaymentInterface(
        id=0,
        type="housin",
        categoria="insurance",
        DN=date(2024, 7, 1),
        DK=date(2025, 7, 1),
        amount=2431.07,
        is_Moscow=False,
        is_payment_transferred=False,
    )
    payment1 = PaymentInterface(
        id=1,
        type="housin",
        categoria="insurance",
        DN=date(2025, 9, 1),
        DK=date(2026, 3, 1),
        amount=2831,
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

    result = calculate_housin(data)
    print(result)
    # for pid, periods in result.items():
    #     print(f"payment id: {pid}")
    #     for p in periods:
    #         print("  ", p)
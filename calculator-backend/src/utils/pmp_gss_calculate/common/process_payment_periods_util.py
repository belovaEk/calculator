import logging
from typing import Dict, List
from datetime import date
from src.constants.gss_pmp_const import PMP_STANDART, GSS_STANDART
from src.utils.payments.types.paymentType import PaymentsByPeriods

from datetime import date
from typing import Dict, List, Optional
from src.utils.payments.pension_amount_util import calculate_sp_standart
from src.schemas.json_query_schema import (
    JsonQuerySchema,
)


def calculate_amount_for_period_pmp(
    start_date: date,
    suspension_dks: List[date],
    standart_dict: Dict[int, float],
    pension_id: int,
    SP_STANDART: PaymentsByPeriods,
    prev_amount: Optional[float] = None,
) -> float:
    """Вычисляет amount для одного периода"""

    # ---- Старый алгоритм (когда SP_STANDART был Dict[int, float]) ----
    # year = start_date.year
    # if start_date.month == 12:
    #     amount = standart_dict[year + 1] - SP_STANDART[pension_id][year]
    # else:
    #     if start_date in suspension_dks:
    #         amount = standart_dict[year] - SP_STANDART[pension_id][year - 1]
    #     else:
    #         amount = standart_dict[year] - SP_STANDART[pension_id][year]
    # if prev_amount is not None and amount <= prev_amount:
    #     amount = prev_amount
    # return round(amount, 2)

    # ---- Новый этап: SP_STANDART = Dict[int, Dict[PeriodType, float]] ----
    pension_periods_map = SP_STANDART.get(pension_id)
    if not pension_periods_map:
        sp_god = 0.0
        sp_god_minus_one = 0.0
    else:
        # Приводим dict[PeriodType, float] к упорядоченному списку периодов (по DN)
        periods_with_amount = sorted(
            pension_periods_map.items(),
            key=lambda item: item[0].DN,
        )

        sp_god = 0.0
        sp_god_minus_one = 0.0

        for idx, (period, amount_value) in enumerate(periods_with_amount):
            if period.DN <= start_date < period.DK:
                sp_god = float(amount_value)
                sp_god_minus_one = (
                    float(periods_with_amount[idx - 1][1]) if idx > 0 else 0.0
                )
                break

    # Пока что только подготовка sp_god / sp_god_minus_one.
    # Дальнейший расчёт amount будет добавлен следующим шагом.
    amount = 0.0
    return round(amount, 2)


def calculate_amount_for_period_gss(
    start_date: date,
    suspension_dks: List[date],
    standart_dict: Dict[int, float],
    pension_id: int,
    SP_STANDART: PaymentsByPeriods,
    prev_amount: Optional[float] = None,
) -> Optional[float]:
    return None


async def process_payment_periods(
    data: JsonQuerySchema,
    periods_data: Dict[str, List[List[date]]],
    suspension_dks: List[date],
    period_type: str,  # "pmp" или "gss"
) -> Dict[str, List[dict]]:
    """
    Обрабатывает периоды для одного типа (PMP или GSS)

    Args:
        periods_data: словарь вида {"0": [[date1,date2,date3], [date4,date5,date6,date7]]}
        suspension_dks: список дат DK из periods_suspension
        period_type: "pmp" или "gss"

    Returns:
        словарь вида {"0": [{"DN": date, "DK": date, "amount": float}, ...]}
    """
    # Выбираем нужный словарь стандартов
    try:
        if period_type == "pmp":
            standart_dict = PMP_STANDART
        elif period_type == "gss":
            standart_dict = GSS_STANDART
        else:
            raise ValueError(f"Неизвестный period_type: {period_type}")
    except ValueError as e:
        logging.error(f"Ошибка при обработке period_type: {e}")
        return {}

    calculate_amount_for_period = (
        calculate_amount_for_period_pmp
        if period_type == "pmp"
        else calculate_amount_for_period_gss
    )

    SP_STANDART = await calculate_sp_standart(data)

    logging.info(f"SP_STANDART: {SP_STANDART}")
    result = {}

    for pension_id, period_lists in periods_data.items():
        pension_periods = []
        prev_amount = None

        for date_list in period_lists:
            # Разрезаем на пары и сразу считаем amount
            for i in range(len(date_list) - 1):
                start = date_list[i]
                end = date_list[i + 1]

                amount = calculate_amount_for_period(
                    start_date=start,
                    suspension_dks=suspension_dks,
                    standart_dict=standart_dict,
                    prev_amount=prev_amount,
                    pension_id=pension_id,
                    SP_STANDART=SP_STANDART,
                )

                pension_periods.append({"DN": start, "DK": end, "amount": amount})

                prev_amount = amount

        result[pension_id] = pension_periods

    return result

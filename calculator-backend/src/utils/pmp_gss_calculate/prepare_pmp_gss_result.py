from src.schemas.json_query_schema import PeriodType, JsonQuerySchema, PaymentInterface
from datetime import date
from typing import List
from src.utils.pmp_gss_calculate.reg.pmp_gss_reg_util import pmp_gss_registration
from src.utils.pmp_gss_calculate.reg.pmp_gss_suspension_util import pmp_gss_suspension
from src.utils.pmp_gss_calculate.reg.pmp_gss_inpatient_util import pmp_gss_inpatient
from src.utils.pmp_gss_calculate.reg.pmp_gss_payment import pmp_gss_pension

# from src.utils.pmp_gss_calculate.reg.pmp_gss_date_index_util import pmp_gss_index
from src.utils.pmp_gss_calculate.reg.pmp_gss_payment_amount import (
    pmp_gss_payment_amount,
)
from src.utils.pmp_gss_calculate.reg.pmp_gss_sorted import pmp_gss_sorted


from src.utils.pmp_gss_calculate.no_reg.pmp_init_util import pmp_init
from src.utils.pmp_gss_calculate.no_reg.pmp_suspension_util import pmp_suspension
from src.utils.pmp_gss_calculate.no_reg.pmp_payment_util import pmp_pension
from src.utils.pmp_gss_calculate.no_reg.pmp_date_index_util import pmp_date_index
from src.utils.pmp_gss_calculate.no_reg.pmp_payment_amount import pmp_payment_amount
from src.utils.pmp_gss_calculate.no_reg.pmp_sorted import pmp_sorted
import logging

from src.utils.dev.alt_pmp_gss_date_index_util import pmp_gss_index
from src.utils.dev.alt_pmp_gss_payment_amount import alt_pmp_gss_payment_amount
from src.utils.dev.alt_pmp_payment_amount import alt_pmp_payment_amount

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,  # Уровень: DEBUG, INFO, WARNING, ERROR, CRITICAL
    format="%(asctime)s - %(levelname)s - %(message)s",  # Формат: время - уровень - сообщение
    handlers=[logging.StreamHandler()],  # Вывод в консоль
)


async def prepare_pmp_gss_reg_result(
    data: JsonQuerySchema,
    sum_reg_10_date: date,
    spv_init_date: date,
    list_of_periods_reg_child: List[PeriodType],
    pmp_periods: List[PeriodType],
    gss_periods: List[PeriodType],
    first_moscow_payment: PaymentInterface,
) -> dict:
    """
    Общая функция для формирования результата с периодами ПМП и ГСС если у ребенка есть регистрация в Москве.
    """
    pmp_gss_registration_result = await pmp_gss_registration(
        dr10=sum_reg_10_date,
        spv_init_date=spv_init_date,
        list_of_periods_reg=list_of_periods_reg_child,
        pmp_periods=pmp_periods,
        gss_periods=gss_periods,
    )

    periods_suspension = data.periods_suspension or None

    pmp_gss_suspension_result = await pmp_gss_suspension(
        periods_suspension=periods_suspension,
        pmp_periods=pmp_gss_registration_result["pmp_periods"],
        gss_periods=pmp_gss_registration_result["gss_periods"],
    )

    pmp_gss_inpatient_result = await pmp_gss_inpatient(
        pmp_periods=pmp_gss_suspension_result["pmp_periods"],
        gss_periods=pmp_gss_suspension_result["gss_periods"],
        periods_inpatient=data.periods_inpatient,
    )

    pmp_gss_pension_result = await pmp_gss_pension(
        data=data,
        pmp_periods=pmp_gss_inpatient_result["pmp_periods"],
        gss_periods=pmp_gss_inpatient_result["gss_periods"],
    )
    # logging.info(f"Периоды gss_pension_result: {pmp_gss_pension_result['gss_periods']}")

    pmp_gss_index_result = await pmp_gss_index(
        pmp_periods=pmp_gss_pension_result["pmp_periods"],
        gss_periods=pmp_gss_pension_result["gss_periods"],
        reg=True,
    )

    alt_pmp_gss_payment_amount_result = await alt_pmp_gss_payment_amount(
        pmp_periods=pmp_gss_index_result["pmp_periods"],
        gss_periods=pmp_gss_index_result["gss_periods"],
        data=data,
    )

    pmp_gss_sorted_result = await pmp_gss_sorted(
        pmp_periods=alt_pmp_gss_payment_amount_result["pmp_periods"],
        gss_periods=alt_pmp_gss_payment_amount_result["gss_periods"],
    )

    return {
        "pmp_periods": pmp_gss_pension_result["pmp_periods"],
        "gss_periods": pmp_gss_pension_result["gss_periods"],
        "sorted_pensions": pmp_gss_sorted_result,
    }


async def prepare_pmp_gss_NoReg_result(
    data: JsonQuerySchema,
    spv_init_date: date,
    pmp_periods: List[PeriodType],
    gss_periods: List[PeriodType],
    first_moscow_payment: PaymentInterface,
) -> dict:
    """
    Общая функция для формирования результата с периодами ПМП если у ребенка нет регистрации в Москве.
    """
    pmp_init_result = await pmp_init(
        data=data,
        pmp_periods=pmp_periods,
    )

    periods_suspension = data.periods_suspension or None
    pmp_suspension_result = await pmp_suspension(
        periods_suspension=periods_suspension,
        pmp_periods=pmp_init_result["pmp_periods"],
        data=data
    )

    pmp_pension_result = await pmp_pension(
        data=data,
        pmp_periods=pmp_suspension_result["pmp_periods"],
    )

    pmp_gss_index_result = await pmp_gss_index(
        pmp_periods=pmp_pension_result["pmp_periods"],
        gss_periods={},
        reg=False,
    )

    # return {
    #     "pmp_periods": pmp_gss_index_result["pmp_periods"],
    #     "gss_periods": pmp_gss_index_result["gss_periods"],
    # }

    alt_pmp_payment_amount_result = await alt_pmp_payment_amount(
        pmp_periods=pmp_gss_index_result["pmp_periods"],
        data=data,
    )

    pmp_sorted_result = await pmp_sorted(
        pmp_periods=alt_pmp_payment_amount_result["pmp_periods"]
    )

    return {
        "pmp_periods": pmp_pension_result["pmp_periods"],
        "sorted_pensions": pmp_sorted_result,
    }

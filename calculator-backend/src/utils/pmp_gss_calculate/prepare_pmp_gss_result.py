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

from src.utils.dev.alt_pmp_gss_date_index_util import pmp_gss_index
from src.utils.dev.alt_pmp_gss_payment_amount import alt_pmp_gss_payment_amount
from src.utils.dev.alt_pmp_payment_amount import alt_pmp_payment_amount

from src.utils.payments.types.paymentType import (
    PaymentsByPeriods
)
from src.utils.payments.pension_amount_util import calculate_sp_standart
from src.utils.pmp_gss_calculate.prepare_pmp_gss_result_adult import convert_period_amount_to_payment_interface
from src.utils.logger import logger, log_function_call, log_execution_time


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
        data=data
    )
    print(f'периоды после регистрации: {pmp_gss_registration_result}')

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
    print(f'периоды ГСС после стационаризации: {pmp_gss_inpatient_result}')

    # pmp_gss_pension_result = await pmp_gss_pension(
    #     data=data,
    #     pmp_periods=pmp_gss_inpatient_result["pmp_periods"],
    #     gss_periods=pmp_gss_inpatient_result["gss_periods"],
    # )
    # logging.info(f"Периоды gss_pension_result: {pmp_gss_pension_result['gss_periods']}")

    pmp_gss_index_result = await pmp_gss_index(
        pmp_periods=pmp_gss_inpatient_result["pmp_periods"],
        gss_periods=pmp_gss_inpatient_result["gss_periods"],
        reg=True,
        data=data,
    )
    print(f'периоды после индексации: {pmp_gss_index_result}')


    sp_standart: PaymentsByPeriods = await calculate_sp_standart(data)

    # Создаем список всех выплат для breakpoint'ов
    all_payments_for_breakpoints = []

    # Преобразуем пенсии
    if sp_standart:
        # pensions_result может быть словарем или списком
        pension_payments = convert_period_amount_to_payment_interface(
            sp_standart, 
            payment_type="pension",
            categoria="insurance"  # или подходящая категория
        )
        all_payments_for_breakpoints.extend(pension_payments)

    # Сохраняем в data.payments
    data.payments = all_payments_for_breakpoints

    alt_pmp_gss_payment_amount_result = await alt_pmp_gss_payment_amount(
        pmp_periods=pmp_gss_index_result["pmp_periods"],
        gss_periods=pmp_gss_index_result["gss_periods"],
        data=data,
        reg=True,
    )
    print(f'периоды после расчета суммы: {alt_pmp_gss_payment_amount_result}')

    pmp_gss_sorted_result = await pmp_gss_sorted(
        pmp_periods=alt_pmp_gss_payment_amount_result["pmp_periods"],
        gss_periods=alt_pmp_gss_payment_amount_result["gss_periods"],
        data=data,
    )


    return {
        "pmp_periods": pmp_gss_inpatient_result["pmp_periods"],
        "gss_periods": pmp_gss_inpatient_result["gss_periods"],
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
    )

    # pmp_pension_result = await pmp_pension(
    #     data=data,
    #     pmp_periods=pmp_suspension_result["pmp_periods"],
    # )

    pmp_gss_index_result = await pmp_gss_index(
        pmp_periods=pmp_suspension_result["pmp_periods"],
        gss_periods={},
        reg=False,
        data=data
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
        "pmp_periods": {0:pmp_suspension_result["pmp_periods"]},
        "sorted_pensions": pmp_sorted_result,
    }

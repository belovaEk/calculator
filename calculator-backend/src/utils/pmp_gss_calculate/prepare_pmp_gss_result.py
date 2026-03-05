from src.schemas.json_query_schema import (
    PeriodType,
    JsonQuerySchema,
    PaymentInterface
)
from datetime import date
from typing import List
from src.utils.pmp_gss_calculate.reg.pmp_gss_reg_util import pmp_gss_registration
from src.utils.pmp_gss_calculate.reg.pmp_gss_suspension_util import pmp_gss_suspension
from src.utils.pmp_gss_calculate.reg.pmp_gss_inpatient_util import pmp_gss_inpatient
from src.utils.pmp_gss_calculate.reg.pmp_gss_payment import pmp_gss_pension
from src.utils.pmp_gss_calculate.reg.pmp_gss_date_index_util import pmp_gss_index
from src.utils.pmp_gss_calculate.reg.pmp_gss_payment_amount import (
    pmp_gss_payment_amount,
)


from src.utils.pmp_gss_calculate.no_reg.pmp_init_util import pmp_init


async def prepare_pmp_gss_reg_result(
    data: JsonQuerySchema,
    sum_reg_10_date: date,
    spv_init_date: date,
    list_of_periods_reg_child: List[PeriodType],
    pmp_periods: List[PeriodType],
    gss_periods: List[PeriodType],
    first_moscow_payment: PaymentInterface
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

    pmp_gss_suspension_result = await pmp_gss_suspension(
        data=data,
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

    pmp_gss_index_result = await pmp_gss_index(
        pmp_periods=pmp_gss_pension_result["pmp_periods"],
        gss_periods=pmp_gss_pension_result["gss_periods"],
    )


    if first_moscow_payment.categoria == "insurance_SPK": 
        pmp_gss_payment_amount_result = await pmp_gss_payment_amount(
            pmp_periods=pmp_gss_index_result["pmp_periods"],
            gss_periods=pmp_gss_index_result["gss_periods"],
            suspension_periods=data.periods_suspension,
            data=data
        )

        return {
            "pmp_periods": pmp_gss_pension_result["pmp_periods"],
            "gss_periods": pmp_gss_pension_result["gss_periods"],
            "pmp_rsd": pmp_gss_payment_amount_result["pmp_periods"],
            "gss_rsd": pmp_gss_payment_amount_result["gss_periods"],
        }

    return {
        "pmp_periods": pmp_gss_pension_result["pmp_periods"],
        "gss_periods": pmp_gss_pension_result["gss_periods"],
        "message": 'Обрабатывается только страховая по СПК'
    }


async def prepare_pmp_gss_NoReg_result(
    data: JsonQuerySchema,
    spv_init_date: date,
    pmp_periods: List[PeriodType],
    gss_periods: List[PeriodType],
    first_moscow_payment: PaymentInterface
) -> dict:
    """
    Общая функция для формирования результата с периодами ПМП если у ребенка нет регистрации в Москве.
    """
    pmp_init_result = await pmp_init(
        data=data,
        pmp_periods=pmp_periods,
    )

    # pmp_gss_suspension_result = await pmp_gss_suspension(
    #     data=data,
    #     pmp_periods=pmp_gss_registration_result["pmp_periods"],
    #     gss_periods=pmp_gss_registration_result["gss_periods"],
    # )

    # pmp_gss_inpatient_result = await pmp_gss_inpatient(
    #     pmp_periods=pmp_gss_suspension_result["pmp_periods"],
    #     gss_periods=pmp_gss_suspension_result["gss_periods"],
    #     periods_inpatient=data.periods_inpatient,
    # )

    # pmp_gss_pension_result = await pmp_gss_pension(
    #     data=data,
    #     pmp_periods=pmp_gss_inpatient_result["pmp_periods"],
    #     gss_periods=pmp_gss_inpatient_result["gss_periods"],
    # )

    # pmp_gss_index_result = await pmp_gss_index(
    #     pmp_periods=pmp_gss_pension_result["pmp_periods"],
    #     gss_periods=pmp_gss_pension_result["gss_periods"],
    # )


    # if first_moscow_payment.categoria == "insurance_SPK": 
    #     pmp_gss_payment_amount_result = await pmp_gss_payment_amount(
    #         pmp_periods=pmp_gss_index_result["pmp_periods"],
    #         gss_periods=pmp_gss_index_result["gss_periods"],
    #         suspension_periods=data.periods_suspension,
    #         data=data
    #     )

    #     return {
    #         "pmp_periods": pmp_gss_pension_result["pmp_periods"],
    #         "gss_periods": pmp_gss_pension_result["gss_periods"],
    #         "pmp_rsd": pmp_gss_payment_amount_result["pmp_periods"],
    #         "gss_rsd": pmp_gss_payment_amount_result["gss_periods"],
    #     }

    return {
        "pmp_periods": pmp_init_result["pmp_periods"],
    }

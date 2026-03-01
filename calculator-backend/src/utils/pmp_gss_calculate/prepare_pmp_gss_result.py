from src.schemas.json_query_schema import (
    PeriodType,
    JsonQuerySchema,
)
from datetime import date
from typing import List
from src.utils.pmp_gss_calculate.pmp_gss_reg_util import pmp_gss_registration
from src.utils.pmp_gss_calculate.pmp_gss_suspension_util import pmp_gss_suspension


async def prepare_pmp_gss_result(
    data: JsonQuerySchema,
    sum_reg_10_date: date,
    spv_init_date: date,
    list_of_periods_reg_child: List[PeriodType],
    pmp_periods: List[PeriodType],
    gss_periods: List[PeriodType],
) -> dict:
    """
    Общая функция для формирования результата с периодами ПМП и ГСС.
    """
    pmp_gss_result = await pmp_gss_registration(
        dr10=sum_reg_10_date,
        spv_init_date=spv_init_date,
        list_of_periods_reg=list_of_periods_reg_child,
        PMP=pmp_periods,
        GSS=gss_periods,
    )

    pmp_gss_suspension_result = await pmp_gss_suspension(
        data=data, pmp_periods=pmp_gss_result["PMP"], gss_periods=pmp_gss_result["GSS"]
    )

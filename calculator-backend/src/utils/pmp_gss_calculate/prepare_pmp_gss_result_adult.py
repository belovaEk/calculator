from datetime import date
from typing import List

from src.schemas.json_query_schema import JsonQuerySchema, PeriodType
from src.utils.pmp_gss_calculate.reg.pmp_gss_reg_util import pmp_gss_registration
from src.utils.pmp_gss_calculate.common.cut_off_periods_util import (
    cut_off_periods_before_change_date, cut_of_order_date
)
from src.utils.pmp_gss_calculate.reg.pmp_gss_inpatient_util import pmp_gss_inpatient
from src.utils.pmp_gss_calculate.adult.employment_to_suspensions_periods import employment_to_suspensions_periods
from src.utils.pmp_gss_calculate.reg.pmp_gss_suspension_util import pmp_gss_suspension
from src.utils.pmp_gss_calculate.adult.transformation_gss_to_pmp_util import transformation_gss_to_pmp

async def prepare_pmp_gss_reg_result_adult(
    data: JsonQuerySchema,
    dr10: date,
    spv_init_date: date,
    list_of_periods_reg: List[PeriodType],
) -> dict:
    """
    Упрощённая функция для взрослых: формирует только периоды ПМП и ГСС
    на основании даты 10 лет регистрации и даты первой СПВ.
    """
    pmp_periods: List[PeriodType] = []
    gss_periods: List[PeriodType] = []

    pmp_gss_registration_result = await pmp_gss_registration(
        dr10=dr10,
        spv_init_date=spv_init_date,
        list_of_periods_reg=list_of_periods_reg,
        pmp_periods=pmp_periods,
        gss_periods=gss_periods,
    )

    return {
        "pmp_periods": pmp_gss_registration_result["pmp_periods"],
        "gss_periods": pmp_gss_registration_result["gss_periods"],
    }


async def prepare_pmp_gss_adult_result(
    data: JsonQuerySchema,
    dr10: date,
    spv_init_date: date,
    list_of_periods_reg: List[PeriodType],
) -> dict:
    """
    Основной пайплайн расчёта для взрослых (аналог связки main_util.py -> prepare_pmp_gss_result.py):
    1) регистрация (pmp_gss_registration) -> pmp_periods/gss_periods
    2) проверка стационаризации (если есть) -> фильтрация периодов
    """
    base_result = await prepare_pmp_gss_reg_result_adult(
        data=data,
        dr10=dr10,
        spv_init_date=spv_init_date,
        list_of_periods_reg=list_of_periods_reg,
    )

    if data.periods_inpatient and len(data.periods_inpatient) > 0:

        filtered_inpatient_periods = await cut_off_periods_before_change_date(
        periods=data.periods_inpatient,
        change_last_date=data.change_last_date,
        )
        
        pmp_gss_inpatient_result = await pmp_gss_inpatient(
            pmp_periods=base_result["pmp_periods"],
            gss_periods=base_result["gss_periods"],
            periods_inpatient=filtered_inpatient_periods,
        )

    
    # if data.is_employment and data.periods_employment and len(data.periods_employment) > 0:
    if data.periods_employment and len(data.periods_employment) > 0:

        filtered_employment_periods = await cut_off_periods_before_change_date(
            periods=data.periods_employment,
            change_last_date=data.change_last_date,
        )

    if data.periods_suspension and len(data.periods_suspension) > 0:


        filtered_suspension_periods = await cut_off_periods_before_change_date(
            periods=data.periods_suspension,
            change_last_date=data.change_last_date,
        )   

        employment_to_suspensions_periods_result = await employment_to_suspensions_periods(
            employment_periods=filtered_employment_periods,
            suspension_periods=filtered_suspension_periods,
        )
    
    else: 
        employment_to_suspensions_periods_result = filtered_employment_periods

    pmp_gss_suspension_result = await pmp_gss_suspension(
        periods_suspension=employment_to_suspensions_periods_result,
        pmp_periods=pmp_gss_inpatient_result["pmp_periods"],
        gss_periods=pmp_gss_inpatient_result["gss_periods"],
    )

    # Следующая_функция_результат = следующая_функция(
        # pmp_periods=pmp_gss_suspension_result["pmp_periods"],
        # gss_periods=pmp_gss_suspension_result["gss_periods"],
        # )

    if data.is_order:
        new_orders_date = await cut_of_order_date(
            orders_date=data.orders_date,
            change_last_date=data.change_last_date
        )
    else:
        gss_to_pmp_result = await transformation_gss_to_pmp(
            pmp_periods=pmp_gss_suspension_result["pmp_periods"],
            gss_periods=pmp_gss_suspension_result["gss_periods"],
        )

        
    return {
        "pmp_periods": pmp_gss_suspension_result["pmp_periods"],
        "gss_periods": pmp_gss_suspension_result["gss_periods"],

    }

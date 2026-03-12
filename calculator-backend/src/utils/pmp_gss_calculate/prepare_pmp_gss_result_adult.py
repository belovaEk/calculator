from datetime import date
from typing import List

from src.schemas.json_query_schema import JsonQuerySchema, PeriodType
from src.utils.pmp_gss_calculate.reg.pmp_gss_reg_util import pmp_gss_registration
from src.utils.pmp_gss_calculate.pmp_gss_inpation_util import (
    filter_inpatient_periods_after_change_date,
)
from src.utils.pmp_gss_calculate.reg.pmp_gss_inpatient_util import pmp_gss_inpatient


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

    if not data.periods_inpatient or len(data.periods_inpatient) == 0:
        return {
            "pmp_periods": base_result["pmp_periods"],
            "gss_periods": base_result["gss_periods"],
        }

    filtered_inpatient = await filter_inpatient_periods_after_change_date(
        periods_inpatient=data.periods_inpatient,
        change_last_date=data.change_last_date,
    )

    pmp_gss_inpatient_result = pmp_gss_inpatient(
        pmp_periods=base_result["pmp_periods"],
        gss_periods=base_result["gss_periods"],
        periods_inpatient=filtered_inpatient
    )

    return {
        "pmp_periods": base_result["pmp_periods"],
        "gss_periods": base_result["gss_periods"],
        "periods_inpatient": filtered_inpatient,
    }

from datetime import date
from typing import List

from src.schemas.json_query_schema import JsonQuerySchema, PeriodType
from src.schemas.json_query_schema import OrderType, PeriodWithIdType
from src.utils.pmp_gss_calculate.reg.pmp_gss_reg_util import pmp_gss_registration
from src.utils.pmp_gss_calculate.common.cut_off_periods_util import (
    cut_of_gss_no_have_order,
    cut_off_periods_before_change_date,
    cut_of_order_date,
)
from src.utils.pmp_gss_calculate.reg.pmp_gss_inpatient_util import pmp_gss_inpatient
from src.utils.pmp_gss_calculate.adult.employment_to_suspensions_periods import (
    employment_to_suspensions_periods,
)
from src.utils.pmp_gss_calculate.reg.pmp_gss_suspension_util import pmp_gss_suspension
from src.utils.pmp_gss_calculate.adult.transformation_gss_to_pmp_util import (
    transformation_gss_to_pmp,
)

from src.utils.payments.edk_calculate import calculate_edk
from src.utils.payments.edv_nsu_calculate import calculate_edv_nsu
from src.utils.payments.egdv_calculate import calculate_egdv
from src.utils.payments.housin_calculate import calculate_housin
from src.utils.payments.pension_summary import calculate_pension_itog
from src.utils.pmp_gss_calculate.reg.pmp_gss_sorted import pmp_gss_sorted
from src.utils.pmp_gss_calculate.adult.build_pensii_itog_res import _build_pensii_itog_res
from src.utils.pmp_gss_calculate.adult.start_OMO import pensii_devochki
from src.utils.dev.alt_pmp_gss_date_index_util import pmp_gss_index
from src.utils.pmp_gss_calculate.adult.pmp_gss_payment_amount_adult import pmp_gss_payment_amount_adult


from src.utils.pmp_gss_calculate.no_reg.pmp_suspension_util import pmp_suspension
from src.utils.pmp_gss_calculate.no_reg.pmp_init_util import pmp_init


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

        base_result = await pmp_gss_inpatient(
            pmp_periods=base_result["pmp_periods"],
            gss_periods=base_result["gss_periods"],
            periods_inpatient=filtered_inpatient_periods,
        )

    filtered_employment_periods: List[PeriodWithIdType] = []
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

        suspensions_w_emploument_periods = (
            await employment_to_suspensions_periods(
                employment_periods=filtered_employment_periods,
                suspension_periods=filtered_suspension_periods,
            )
        )

    else:
        suspensions_w_emploument_periods = filtered_employment_periods

        base_result = await pmp_gss_suspension(
        periods_suspension=suspensions_w_emploument_periods,
        pmp_periods=base_result["pmp_periods"],
        gss_periods=base_result["gss_periods"],
    )



    if data.is_order:
        new_orders_date = await cut_of_order_date(
            orders_date=data.orders_date, change_last_date=data.change_last_date
        )
        base_result = await cut_of_gss_no_have_order(
            pmp_periods=base_result["pmp_periods"],
            gss_period=base_result["gss_periods"],
            orders_date=new_orders_date,
        )
    else:
        base_result = await transformation_gss_to_pmp(
            pmp_periods=base_result["pmp_periods"],
            gss_periods=base_result["gss_periods"],
        )


    pmp_gss_index_result = await pmp_gss_index(
        gss_periods= {0: base_result["gss_periods"]},
        pmp_periods= {0: base_result["pmp_periods"]},
        reg=True
    )

    # Расчёт дополнительных федеральных/региональных выплат
    edk_result = calculate_edk(data)
    edv_result = calculate_edv_nsu(data)
    egdv_result = calculate_egdv(data)
    housin_result = calculate_housin(data)
    pensions_result = pensii_devochki(query=data)

    # # Итоговая агрегация всех выплат в единую хронологию
    payments_for_pmp = _build_pensii_itog_res(
        sorted_pensions=pensions_result,
        edk=edk_result,
        edv=edv_result,
        egdv=egdv_result,
        housing=housin_result,
    )
    # payments_for_pmp - для pmp_periods

    payments_for_gss = _build_pensii_itog_res(
        sorted_pensions=pensions_result
    )
    # payments_for_gss - для gss_periods

    omo_pmp = calculate_pension_itog(payments_for_pmp)
    omo_gss = calculate_pension_itog(payments_for_gss)
    # Передаем в функицю по аналогии с sp_standart
    # return {
    #     'payments_for_gss': payments_for_gss,
    #     "omo_pmp": omo_pmp,
    # }


    alt_pmp_gss_payment_amount_result = await pmp_gss_payment_amount_adult(
        pmp_periods=pmp_gss_index_result["pmp_periods"],
        gss_periods=pmp_gss_index_result["gss_periods"],
        omo_pmp=omo_pmp,
        omo_gss=omo_gss,
        data=data
    )

    pmp_gss_sorted_result = await pmp_gss_sorted(
        pmp_periods=alt_pmp_gss_payment_amount_result["pmp_periods"],
        gss_periods=alt_pmp_gss_payment_amount_result["gss_periods"],
    )

    
    return {
        'devochki': pensions_result,
        "pmp_periods": pmp_gss_index_result["pmp_periods"],
        "gss_periods": pmp_gss_index_result["gss_periods"],
        "sorted_pensions": pmp_gss_sorted_result,
    }


async def prepare_pmp_adult_result(
    data: JsonQuerySchema,
) -> dict:
    """

    """
    pmp_periods: List[PeriodType] = []

    base_result = await pmp_init(
        data=data,
        pmp_periods=pmp_periods,
    )

    filtered_employment_periods: List[PeriodWithIdType] = []

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

        suspensions_w_emploument_periods = (
            await employment_to_suspensions_periods(
                employment_periods=filtered_employment_periods,
                suspension_periods=filtered_suspension_periods,
            )
        )

    else:
        suspensions_w_emploument_periods = filtered_employment_periods

        base_result = await pmp_suspension(
        periods_suspension=suspensions_w_emploument_periods,
        pmp_periods=base_result["pmp_periods"]
    )


    pmp_gss_index_result = await pmp_gss_index(
        gss_periods= {},
        pmp_periods= {0: base_result["pmp_periods"]},
        reg=False
    )

    # Расчёт дополнительных федеральных/региональных выплат
    edk_result = calculate_edk(data)
    edv_result = calculate_edv_nsu(data)
    egdv_result = calculate_egdv(data)
    housin_result = calculate_housin(data)
    pensions_result = pensii_devochki(query=data)

    payments_for_pmp = _build_pensii_itog_res(
        sorted_pensions=pensions_result,
        edk=edk_result,
        edv=edv_result,
        egdv=egdv_result,
        housing=housin_result,
    )

    payments_for_gss = _build_pensii_itog_res(
        sorted_pensions=pensions_result
    )


    omo_pmp = calculate_pension_itog(payments_for_pmp)
    # omo_gss = calculate_pension_itog(payments_for_gss)
    omo_gss = {}

    alt_pmp_gss_payment_amount_result = await pmp_gss_payment_amount_adult(
        pmp_periods=pmp_gss_index_result["pmp_periods"],
        gss_periods={},
        omo_pmp=omo_pmp,
        omo_gss=omo_gss,
        data=data
    )

    pmp_gss_sorted_result = await pmp_gss_sorted(
        pmp_periods=alt_pmp_gss_payment_amount_result["pmp_periods"],
        gss_periods={},
    )

    
    return {
        'devochki': pensions_result,
        "pmp_periods": pmp_gss_index_result["pmp_periods"],
        "gss_periods": pmp_gss_index_result["gss_periods"],
        "sorted_pensions": pmp_gss_sorted_result,
    }
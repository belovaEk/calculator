from src.schemas.json_query_schema import (
    JsonQuerySchema,
    PeriodType,
    PaymentInterface,
)
from dateutil.relativedelta import relativedelta
from datetime import date
from typing import List
from src.utils.registration.registration_util import (
    calculate_total_registration_without_breaks,
)
from src.utils.payment_util import get_first_moscow_pension
from src.utils.pmp_gss_calculate.prepare_pmp_gss_result_adult import (
    prepare_pmp_gss_adult_result,
)


async def main_util_adult(data: JsonQuerySchema) -> dict:
    """
    Главная функция для расчета взрослых.
    """

    today = date.today()

    # Если дата последнего изменения вида пенсии не передана,
    # дальнейшую логику выполнить нельзя.
    if not data.change_last_date:
        return {"message": "Не передана дата последнего изменения вида пенсии"}

    # Блок-схема: "текущая дата - дата последнего изменения вида пенсии > 1 месяца"
    spv_delta = relativedelta(today, data.change_last_date)

    # Ветка "нет": считаем только будущие периоды
    if spv_delta.years == 0 and spv_delta.months == 0:
        return {
            "message": "С даты последнего изменения вида пенсии прошло менее 1 месяца, считаем будущие периоды"
        }

    # Ветка "да": проверяем предыдущий период регистрации в Москве
    if not data.is_there_a_registration_in_moscow or not data.periods_reg_moscow:
        return {"message": "Нет периодов регистрации в Москве для взрослого"}

    # Берём последний период регистрации в Москве
    last_period: PeriodType = data.periods_reg_moscow[-1]

    if last_period.DK > today:
        last_period.DK = today

    # Проверяем, есть ли суммарно 10 лет регистрации в Москве
    registration_result = await calculate_total_registration_without_breaks(
        data.periods_reg_moscow
    )

    # Если 10 лет нет — по условию возвращаем вывод, что РСД до ГСС не положено
    if not registration_result["has_10_years"]:
        return {"message": "Вывод: не положено РСД до ГСС"}

    # Если 10 лет есть — считаем периоды ПМП и ГСС через prepare_pmp_gss_reg_result_adult
    dr10 = registration_result["date_of_10_years"]

    spv_init_date = data.change_last_date

    return await prepare_pmp_gss_adult_result(
        data=data,
        dr10=dr10,
        spv_init_date=spv_init_date,
        list_of_periods_reg=data.periods_reg_moscow,
    )

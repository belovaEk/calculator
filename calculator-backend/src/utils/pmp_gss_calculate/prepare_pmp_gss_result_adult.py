from datetime import date
from typing import List

from src.schemas.json_query_schema import JsonQuerySchema, PeriodType
from src.schemas.json_query_schema import OrderType, PeriodWithIdType
from src.utils.payments.types.paymentType import PeriodAmount
from src.schemas.json_query_schema import PaymentInterface
from src.utils.pmp_gss_calculate.reg.pmp_gss_reg_util import pmp_gss_registration
from src.utils.pmp_gss_calculate.common.cut_off_periods_util import (
    cut_of_gss_no_have_order,
    cut_off_periods_before_change_date,
    cut_of_order_date,
    adjust_employment_periods
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

def ensure_periods_list(data):
    """Преобразует данные в список объектов PeriodType"""
    if not data:
        return []
    
    result = []
    for item in data:
        if isinstance(item, PeriodType):
            result.append(item)
        elif isinstance(item, dict):
            try:
                result.append(PeriodType(**item))
            except:
                print(f"Failed to convert dict to PeriodType: {item}")
        elif isinstance(item, (list, tuple)) and len(item) >= 2:
            try:
                result.append(PeriodType(DN=item[0], DK=item[1]))
            except:
                print(f"Failed to convert list to PeriodType: {item}")
        elif hasattr(item, 'DN') and hasattr(item, 'DK'):
            result.append(item)
        else:
            print(f"Skipping invalid period data: {item} (type: {type(item)})")
    
    return result

def ensure_list(data):
    """Преобразует словарь или другой тип в список"""
    if isinstance(data, list):
        return data
    elif isinstance(data, dict):
        # Объединяем все значения словаря в один список
        result = []
        for value in data.values():
            if isinstance(value, list):
                result.extend(value)
            else:
                result.append(value)
        return result
    else:
        return [data] if data else []

def dict_to_list(data):
        """Преобразует словарь вида {0: [...], 1: [...]} в плоский список"""
        if not data:
            return []
        
        if isinstance(data, dict):
            result = []
            for key, value in data.items():
                if isinstance(value, list):
                    result.extend(value)
                elif value is not None:
                    result.append(value)
            return result
        elif isinstance(data, list):
            return data
        else:
            return [data] if data else []


def clean_periods_list(data, name=""):
    """Очищает список от чисел и None, оставляя только объекты PeriodType"""
    # Сначала преобразуем словари в списки
    data = dict_to_list(data)
        
    if not data:
        return []
        
    cleaned = []
    for idx, item in enumerate(data):
        # Пропускаем числа и None
        if isinstance(item, (int, float)):
            print(f"Removing number {item} from {name} at index {idx}")
            continue
        if item is None:
            print(f"Removing None from {name} at index {idx}")
            continue
            
        # Если это уже объект PeriodType
        if isinstance(item, PeriodType):
            cleaned.append(item)
        # Если это объект с атрибутами DN и DK
        elif hasattr(item, 'DN') and hasattr(item, 'DK'):
            cleaned.append(item)
        # Если это словарь
        elif isinstance(item, dict):
            try:
                # Проверяем наличие ключей DN и DK
                if 'DN' in item and 'DK' in item:
                    cleaned.append(PeriodType(DN=item['DN'], DK=item['DK']))
                else:
                    cleaned.append(PeriodType(**item))
            except Exception as e:
                print(f"Failed to convert dict in {name}: {e}")
        # Если это список [DN, DK]
        elif isinstance(item, (list, tuple)) and len(item) >= 2:
            try:
                cleaned.append(PeriodType(DN=item[0], DK=item[1]))
            except Exception as e:
                print(f"Failed to convert list in {name}: {e}")
        else:
            print(f"Unknown type in {name}: {type(item)} - {item}")
        
    return cleaned


def convert_period_amount_to_payment_interface(
    period_amounts: dict, 
    payment_type: str, 
    categoria: str = "other"
) -> List[PaymentInterface]:
    """
    Преобразует словарь PeriodAmount в список PaymentInterface
    """
    result = []
    
    if not period_amounts:
        return result
    
    # Правильное отображение типов
    type_mapping = {
        "housin": "housing",  # housin -> housing
        "pension": "pension",
        "edv": "edv",
        "egdv": "egdv",
        "edk": "edk"
    }
    
    # Используем правильное значение типа
    mapped_type = type_mapping.get(payment_type, payment_type)
    
    if isinstance(period_amounts, dict):
        for key, periods in period_amounts.items():
            for period in periods:
                if isinstance(period, PeriodAmount):
                    payment = PaymentInterface(
                        id=0,
                        type=mapped_type,  # используем mapped_type вместо payment_type
                        categoria=categoria,
                        DN=period.DN,
                        DK=period.DK,
                        amount=period.amount,
                        is_Moscow=True,
                        is_payment_transferred=False
                    )
                    result.append(payment)
    elif isinstance(period_amounts, list):
        for period in period_amounts:
            if isinstance(period, PeriodAmount):
                payment = PaymentInterface(
                    id=0,
                    type=mapped_type,
                    categoria=categoria,
                    DN=period.DN,
                    DK=period.DK,
                    amount=period.amount,
                    is_Moscow=True,
                    is_payment_transferred=False
                )
                result.append(payment)
    
    return result

from src.utils.pmp_gss_calculate.no_reg.pmp_suspension_util import pmp_suspension
from src.utils.pmp_gss_calculate.no_reg.pmp_init_util import pmp_init

def ensure_periods_list(data):
    """Преобразует данные в список объектов PeriodType"""
    if not data:
        return []
    
    result = []
    for item in data:
        if isinstance(item, PeriodType):
            result.append(item)
        elif isinstance(item, dict):
            try:
                result.append(PeriodType(**item))
            except:
                print(f"Failed to convert dict to PeriodType: {item}")
        elif isinstance(item, (list, tuple)) and len(item) >= 2:
            try:
                result.append(PeriodType(DN=item[0], DK=item[1]))
            except:
                print(f"Failed to convert list to PeriodType: {item}")
        elif hasattr(item, 'DN') and hasattr(item, 'DK'):
            result.append(item)
        else:
            print(f"Skipping invalid period data: {item} (type: {type(item)})")
    
    return result

def ensure_list(data):
    """Преобразует словарь или другой тип в список"""
    if isinstance(data, list):
        return data
    elif isinstance(data, dict):
        # Объединяем все значения словаря в один список
        result = []
        for value in data.values():
            if isinstance(value, list):
                result.extend(value)
            else:
                result.append(value)
        return result
    else:
        return [data] if data else []

def dict_to_list(data):
        """Преобразует словарь вида {0: [...], 1: [...]} в плоский список"""
        if not data:
            return []
        
        if isinstance(data, dict):
            result = []
            for key, value in data.items():
                if isinstance(value, list):
                    result.extend(value)
                elif value is not None:
                    result.append(value)
            return result
        elif isinstance(data, list):
            return data
        else:
            return [data] if data else []


def clean_periods_list(data, name=""):
    """Очищает список от чисел и None, оставляя только объекты PeriodType"""
    # Сначала преобразуем словари в списки
    data = dict_to_list(data)
        
    if not data:
        return []
        
    cleaned = []
    for idx, item in enumerate(data):
        # Пропускаем числа и None
        if isinstance(item, (int, float)):
            print(f"Removing number {item} from {name} at index {idx}")
            continue
        if item is None:
            print(f"Removing None from {name} at index {idx}")
            continue
            
        # Если это уже объект PeriodType
        if isinstance(item, PeriodType):
            cleaned.append(item)
        # Если это объект с атрибутами DN и DK
        elif hasattr(item, 'DN') and hasattr(item, 'DK'):
            cleaned.append(item)
        # Если это словарь
        elif isinstance(item, dict):
            try:
                # Проверяем наличие ключей DN и DK
                if 'DN' in item and 'DK' in item:
                    cleaned.append(PeriodType(DN=item['DN'], DK=item['DK']))
                else:
                    cleaned.append(PeriodType(**item))
            except Exception as e:
                print(f"Failed to convert dict in {name}: {e}")
        # Если это список [DN, DK]
        elif isinstance(item, (list, tuple)) and len(item) >= 2:
            try:
                cleaned.append(PeriodType(DN=item[0], DK=item[1]))
            except Exception as e:
                print(f"Failed to convert list in {name}: {e}")
        else:
            print(f"Unknown type in {name}: {type(item)} - {item}")
        
    return cleaned


def convert_period_amount_to_payment_interface(
    period_amounts: dict, 
    payment_type: str, 
    categoria: str = "other"
) -> List[PaymentInterface]:
    """
    Преобразует словарь PeriodAmount в список PaymentInterface
    """
    result = []
    
    if not period_amounts:
        return result
    
    # Правильное отображение типов
    type_mapping = {
        "housin": "housing",  # housin -> housing
        "pension": "pension",
        "edv": "edv",
        "egdv": "egdv",
        "edk": "edk"
    }
    
    # Используем правильное значение типа
    mapped_type = type_mapping.get(payment_type, payment_type)
    
    if isinstance(period_amounts, dict):
        for key, periods in period_amounts.items():
            for period in periods:
                if isinstance(period, PeriodAmount):
                    payment = PaymentInterface(
                        id=0,
                        type=mapped_type,  # используем mapped_type вместо payment_type
                        categoria=categoria,
                        DN=period.DN,
                        DK=period.DK,
                        amount=period.amount,
                        is_Moscow=True,
                        is_payment_transferred=False
                    )
                    result.append(payment)
    elif isinstance(period_amounts, list):
        for period in period_amounts:
            if isinstance(period, PeriodAmount):
                payment = PaymentInterface(
                    id=0,
                    type=mapped_type,
                    categoria=categoria,
                    DN=period.DN,
                    DK=period.DK,
                    amount=period.amount,
                    is_Moscow=True,
                    is_payment_transferred=False
                )
                result.append(payment)
    
    return result

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
        data=data
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

    # Обработка стационарных периодов
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

    # Фильтрация периодов трудоустройства
    filtered_employment_periods: List[PeriodWithIdType] = []
    if data.periods_employment and len(data.periods_employment) > 0:
        filtered_employment_periods = await cut_off_periods_before_change_date(
            periods=data.periods_employment,
            change_last_date=data.change_last_date,
        )

    # Фильтрация периодов трудоустройства
    filtered_employment_periods: List[PeriodWithIdType] = []
    if data.periods_employment and len(data.periods_employment) > 0:
        filtered_employment_periods = await cut_off_periods_before_change_date(
            periods=data.periods_employment,
            change_last_date=data.change_last_date,
    )

    # ДОБАВЬТЕ ЭТО: Преобразуем даты трудоустройства в 1 число следующего месяца
    filtered_employment_periods = await adjust_employment_periods(filtered_employment_periods)

    # Обработка периодов приостановок
    if data.periods_suspension and len(data.periods_suspension) > 0:
        filtered_suspension_periods = await cut_off_periods_before_change_date(
            periods=data.periods_suspension,
            change_last_date=data.change_last_date,
        )

        suspensions_w_emploument_periods = await employment_to_suspensions_periods(
            employment_periods=filtered_employment_periods,
            suspension_periods=filtered_suspension_periods,
        )
    else:
        # Если нет периодов приостановок, используем преобразованные периоды трудоустройства
        suspensions_w_emploument_periods = filtered_employment_periods

    
      
    # Очищаем все данные (теперь функция обрабатывает словари)
    base_result["pmp_periods"] = clean_periods_list(base_result["pmp_periods"], "pmp_periods")
    base_result["gss_periods"] = clean_periods_list(base_result["gss_periods"], "gss_periods")
    suspensions_w_emploument_periods = clean_periods_list(suspensions_w_emploument_periods, "suspensions")

    
    # Если все еще пусто, выводим дополнительную информацию
    if len(base_result['pmp_periods']) == 0:
        print(f"Original pmp_periods data: {base_result['pmp_periods']}")
    if len(base_result['gss_periods']) == 0:
        print(f"Original gss_periods data: {base_result['gss_periods']}")

    # Теперь вызываем
    base_result = await pmp_gss_suspension(
        periods_suspension=suspensions_w_emploument_periods,
        pmp_periods=base_result["pmp_periods"],
        gss_periods=base_result["gss_periods"],
    )
    # Обработка ордеров
    if data.is_order:
        new_orders_date = await cut_of_order_date(
            orders_date=data.orders_date, change_last_date=data.change_last_date
        )
        
        # Преобразуем в списки
        pmp_periods_clean = ensure_list(base_result["pmp_periods"])
        gss_periods_clean = ensure_list(base_result["gss_periods"])
        
        base_result = await cut_of_gss_no_have_order(
            pmp_periods=pmp_periods_clean,
            gss_period=gss_periods_clean,
            orders_date=new_orders_date,
        )
    else:
        # Преобразуем в списки
        pmp_periods_clean = ensure_list(base_result["pmp_periods"])
        gss_periods_clean = ensure_list(base_result["gss_periods"])
        
        base_result = await transformation_gss_to_pmp(
            gss_periods=gss_periods_clean,
            pmp_periods=pmp_periods_clean,
        )

    # Убираем дублирование и используем правильные данные
    pmp_gss_index_result = await pmp_gss_index( 
        gss_periods=ensure_list(base_result["gss_periods"]),
        pmp_periods=ensure_list(base_result["pmp_periods"]),
        reg=True,
        data=data)

    # Расчёт дополнительных федеральных/региональных выплат
    edk_result = calculate_edk(data)
    edv_result = calculate_edv_nsu(data)
    egdv_result = calculate_egdv(data)
    housin_result = calculate_housin(data)
    pensions_result = pensii_devochki(query=data)

    # Итоговая агрегация всех выплат в единую хронологию
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
    omo_gss = calculate_pension_itog(payments_for_gss)
    

    # Создаем список всех выплат для breakpoint'ов
    # В prepare_pmp_gss_adult_result, перед вызовом pmp_gss_payment_amount_adult:

    # Создаем список всех выплат для breakpoint'ов
    all_payments_for_breakpoints = []

    # Преобразуем пенсии
    if pensions_result:
        # pensions_result может быть словарем или списком
        pension_payments = convert_period_amount_to_payment_interface(
            pensions_result, 
            payment_type="pension",
            categoria="insurance"  # или подходящая категория
        )
        all_payments_for_breakpoints.extend(pension_payments)
 
    # Преобразуем EDK
    if edk_result:
        edk_payments = convert_period_amount_to_payment_interface(
            edk_result, 
            payment_type="edk",
            categoria="other"
        )
        all_payments_for_breakpoints.extend(edk_payments)
 
    # Преобразуем EDV
    if edv_result:
        edv_payments = convert_period_amount_to_payment_interface(
            edv_result, 
            payment_type="edv",
            categoria="other"
        )
        all_payments_for_breakpoints.extend(edv_payments)
      
    # Преобразуем EGDV
    if egdv_result:
        egdv_payments = convert_period_amount_to_payment_interface(
            egdv_result, 
            payment_type="egdv",
            categoria="other"
        )
        all_payments_for_breakpoints.extend(egdv_payments)
        
    # Преобразуем Housin
    # Преобразуем Housin - используем "housin" для ключа, но функция сама преобразует в "housing"
    if housin_result:
        housin_payments = convert_period_amount_to_payment_interface(
            housin_result, 
            payment_type="housin",  # используем "housin", функция преобразует в "housing"
            categoria="other"
        )
        all_payments_for_breakpoints.extend(housin_payments)
        

    # Сохраняем в data.payments
    # Сохранить в другое место, поменять обращение
    # в функции pmp_gss_payment_amount_adult
    data.payments = all_payments_for_breakpoints




    # Теперь вызываем pmp_gss_payment_amount_adult
    alt_pmp_gss_payment_amount_result = await pmp_gss_payment_amount_adult(
        pmp_periods=pmp_gss_index_result["pmp_periods"],
        gss_periods=pmp_gss_index_result["gss_periods"],
        omo_pmp=omo_pmp,
        omo_gss=omo_gss,
        data=data,
        reg=True,
    )

    pmp_gss_sorted_result = await pmp_gss_sorted(
        pmp_periods=alt_pmp_gss_payment_amount_result["pmp_periods"],
        gss_periods=alt_pmp_gss_payment_amount_result["gss_periods"],
        data=data
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
        pmp_periods=base_result["pmp_periods"],
        reg=False,
        data=data
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

    omo_pmp = calculate_pension_itog(payments_for_pmp)

    alt_pmp_gss_payment_amount_result = await pmp_gss_payment_amount_adult(
        pmp_periods=pmp_gss_index_result["pmp_periods"],
        gss_periods={},
        omo_pmp=omo_pmp,
        omo_gss={},
        data=data,
        reg=False,
    )

    pmp_gss_sorted_result = await pmp_gss_sorted(
        pmp_periods=alt_pmp_gss_payment_amount_result["pmp_periods"],
        gss_periods={},
        data=data
    )

    
    return {
        "pmp_periods": pmp_gss_index_result["pmp_periods"],
        "sorted_pensions": pmp_gss_sorted_result,
    }
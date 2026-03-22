from src.constants.payment_const import SOCIAL_PENSION_INDEX, INSURANCE_PENSION_SCORE, INSURANCE_PENSION_FIX_AMOUNT
from datetime import date

from src.utils.payments.types.paymentType import (PaymentsByPeriods, PaymentsByPeriodsItem, PeriodAmount)
from src.schemas.json_query_schema import (
    JsonQuerySchema, PaymentInterface
)

def get_score_fix_amount_insurance(DNpen: date):
    target_score = 0
    target_fix_amount = 0
    
    for current_date, score in INSURANCE_PENSION_SCORE.items():
        if current_date <= DNpen:
            target_score = score
            target_fix_amount = INSURANCE_PENSION_FIX_AMOUNT[current_date]
        else:
            break
    return {
            'score': target_score,
            'fix_amount': target_fix_amount
        }


async def calculate_sp_standart(data: JsonQuerySchema) -> PaymentsByPeriods:
    """ Функция по расчета стандартных выплат пенсии по годам

    Returns:
        PaymentsByYear: {   
            0: {
                is_payment_transferred: true
                is_get_PSD_FSD_last_mounth_payment_trasferred: bool
                is_get_PSD_FSD_last_year_payment_trasferred: bool
                is_Not_get_PSD_FSD_now_payment_trasferred: bool
                type: PensionCategoryRaw
                periods:[
                    {DN, DK, amount}, 
                    {DN, DK, amount}
                ]
            };
        }
    """    

    pensions = [p for p in data.payments if p.type == 'pension']
    pensions = [p for p in pensions if p.is_Moscow == True]

    aggregated_flags = {
        'is_payment_transferred': False,
        'is_get_PSD_FSD_last_mounth_payment_trasferred': False,
        'is_get_PSD_FSD_last_year_payment_trasferred': False,
        'is_Not_get_PSD_FSD_now_payment_trasferred': False
    }
    sp_standart_by_year: PaymentsByPeriods = {}

    all_periods = []

    for pension in pensions:
        temp_result = None

        if pension.categoria == "insurance_SPK":
             temp_result = await pension_insurance_SPK_calculate(pension=pension, sp_standart_by_year=sp_standart_by_year)
        elif pension.categoria == "social_SPK" or pension.categoria == "social_disability":
            temp_result = await pension_social_calculate(pension=pension, sp_standart_by_year=sp_standart_by_year)
        elif pension.categoria == "departmental":
            temp_result = await pension_departmental_calculate(pension=pension, sp_standart_by_year=sp_standart_by_year)
 
        last_type = pension.categoria


        if temp_result and 0 in temp_result:
            # Объединяем флаги (если хоть один True, то будет True)
            item = temp_result[0]
            aggregated_flags['is_payment_transferred'] = aggregated_flags['is_payment_transferred'] or item.is_payment_transferred
            aggregated_flags['is_get_PSD_FSD_last_mounth_payment_trasferred'] = aggregated_flags['is_get_PSD_FSD_last_mounth_payment_trasferred'] or item.is_get_PSD_FSD_last_mounth_payment_trasferred
            aggregated_flags['is_get_PSD_FSD_last_year_payment_trasferred'] = aggregated_flags['is_get_PSD_FSD_last_year_payment_trasferred'] or item.is_get_PSD_FSD_last_year_payment_trasferred
            aggregated_flags['is_Not_get_PSD_FSD_now_payment_trasferred'] = aggregated_flags['is_Not_get_PSD_FSD_now_payment_trasferred'] or item.is_Not_get_PSD_FSD_now_payment_trasferred
    
        all_periods.extend(item.periods)

    all_periods.sort(key=lambda x: x.DN)

    sp_standart_by_year[0] = PaymentsByPeriodsItem(
        is_payment_transferred=aggregated_flags['is_payment_transferred'],
        is_get_PSD_FSD_last_mounth_payment_trasferred=aggregated_flags['is_get_PSD_FSD_last_mounth_payment_trasferred'],
        is_get_PSD_FSD_last_year_payment_trasferred=aggregated_flags['is_get_PSD_FSD_last_year_payment_trasferred'],
        is_Not_get_PSD_FSD_now_payment_trasferred=aggregated_flags['is_Not_get_PSD_FSD_now_payment_trasferred'],
        type=last_type, 
        periods=all_periods
    )
    
    return sp_standart_by_year
    


async def pension_insurance_SPK_calculate(pension: PaymentInterface, sp_standart_by_year) -> PaymentsByPeriods:

    """ Функция по расчета стандартных выплат по страховой пенсии по годам

    Returns:
        PaymentsByYear: Возвращает словаь с индексом пенсии, которому принадлежит словарь с годами и соотвествующими стандартными выплатами
    """ 
    
    DNpen = pension.DN
    DKpen = pension.DK
    year = DNpen.year
    summa = pension.amount

    score_fix = get_score_fix_amount_insurance(DNpen)
    score = score_fix['score']
    fix_amount = score_fix['fix_amount']


    sp_standart_by_year[0] = PaymentsByPeriodsItem(
        is_payment_transferred=pension.is_payment_transferred,
        is_get_PSD_FSD_last_mounth_payment_trasferred=pension.is_get_PSD_FSD_last_mounth_payment_trasferred,
        is_get_PSD_FSD_last_year_payment_trasferred=pension.is_get_PSD_FSD_last_year_payment_trasferred,
        is_Not_get_PSD_FSD_now_payment_trasferred=pension.is_Not_get_PSD_FSD_now_payment_trasferred,
        type=pension.categoria, 
        periods=[]
    )

    isRSD = True

    if (score != 0 and fix_amount != 0):
        IPK = (pension.amount - (fix_amount / 2)) / score

    else:
        print("Даты вне заданных периодов ")
        return 
    

    if DNpen.month == 12 and DNpen.day != 31:
        # Если пенсия началась не с конца декабря, добавляем период до конца года
        sp_standart_by_year[0].periods.append(PeriodAmount(DN=DNpen, DK=date(year, 12, 31), amount=summa))
        print(sp_standart_by_year)
        summa = IPK * INSURANCE_PENSION_SCORE[date(DNpen.year+1, 1, 1)] + INSURANCE_PENSION_FIX_AMOUNT[date(DNpen.year+1, 1, 1)]/2
        # Следующий период начинается с 1 января следующего года
        date_for_period = date(year + 1, 1, 1)
        date_index = date(DNpen.year+1, 12, 31) #
    else:
        if pension.is_payment_transferred:
            if pension.is_get_PSD_FSD_last_mounth_payment_trasferred and pension.is_get_PSD_FSD_last_year_payment_trasferred:
                if pension.is_Not_get_PSD_FSD_now_payment_trasferred:
                    sp_prev = IPK*INSURANCE_PENSION_SCORE[date(DNpen.year-1, 1, 1)] + INSURANCE_PENSION_FIX_AMOUNT[date(DNpen.year-1, 1, 1)]/2
                    sp_standart_by_year[0].periods.append(PeriodAmount(DN=date(DNpen.year-1, 12, 31), DK=DNpen, amount=sp_prev))
                else:
                    isRSD = False

        # Текущий период начинается с DNpen            
        date_for_period = DNpen
        summa = pension.amount

        # Определяем следующую дату индексации (конец года)
        date_index = date(DNpen.year, 12, 31) #


    # Обрабатываем последующие периоды
    while date_index < DKpen:
        if isRSD:
            sp_standart_by_year[0].periods.append(PeriodAmount(DN=date_for_period, DK=date_index, amount=summa))
        else:
            sp_standart_by_year[0].periods.append(PeriodAmount(DN=date_for_period, DK=date_index, amount=0))
        
        # Следующий период начинается с 1 января следующего года
        date_for_period = date(date_index.year +1, 1, 1)
        summa = IPK*INSURANCE_PENSION_SCORE[date(date_index.year+1, 1, 1)]+INSURANCE_PENSION_FIX_AMOUNT[date(date_index.year+1, 1, 1)] / 2
        date_index = date(date_for_period.year, 12, 31)
    
    # Добавляем последний период
    if isRSD:
            sp_standart_by_year[0].periods.append(PeriodAmount(DN=date_for_period, DK=DKpen, amount=summa))
    else:
        sp_standart_by_year[0].periods.append(PeriodAmount(DN=date_for_period, DK=DKpen, amount=0))

    return sp_standart_by_year



async def pension_social_calculate(pension: PaymentInterface, sp_standart_by_year) -> PaymentsByPeriods:

    """ Функция по расчета стандартных выплат по социальной пенсии по годам

    Returns:
        PaymentsByYear: Возвращает словаь с индексом пенсии, которому принадлежит словарь с периодами и соотвествующими стандартными выплатами
    """ 


    DNpen = pension.DN
    DKpen = pension.DK

    year = DNpen.year
    summa = pension.amount

    date_for_period = DNpen

    sp_standart_by_year[0] = PaymentsByPeriodsItem(
        is_payment_transferred=pension.is_payment_transferred,
        is_get_PSD_FSD_last_mounth_payment_trasferred=pension.is_get_PSD_FSD_last_mounth_payment_trasferred,
        is_get_PSD_FSD_last_year_payment_trasferred=pension.is_get_PSD_FSD_last_year_payment_trasferred,
        is_Not_get_PSD_FSD_now_payment_trasferred=pension.is_Not_get_PSD_FSD_now_payment_trasferred,
        type=pension.categoria, 
        periods=[]
    )

    isRSD = True

    # определяем дату индексации
    date_index = date(DNpen.year, 4, 1)

    if DNpen > date_index:
        if pension.is_payment_transferred:
            print(44)
            if pension.is_get_PSD_FSD_last_mounth_payment_trasferred and pension.is_get_PSD_FSD_last_year_payment_trasferred:
                if pension.is_Not_get_PSD_FSD_now_payment_trasferred:
                    sp_standart_by_year[0].periods.append(PeriodAmount(DN=date(year-1, 12, 1), DK=DNpen, amount= summa / SOCIAL_PENSION_INDEX[date_index])) 
                    date_for_period = DNpen               
                else:
                    print(45)

                    isRSD = False # РСД не положено
                    sp_standart_by_year[0].periods.append(PeriodAmount(DN=DNpen, DK=date_index, amount=0))
        else:
            date_for_period = DNpen
    else:
        
        if DNpen == date_index:
            date_index = date(DNpen.year+1, DNpen.month, DNpen.day)
            sp_standart_by_year[0].periods.append(PeriodAmount(DN=DNpen, DK=date_index, amount=summa))
            summa = summa*SOCIAL_PENSION_INDEX[date_index]
            date_for_period = date_index

        sp_standart_by_year[0].periods.append(PeriodAmount(DN=DNpen, DK=date_index, amount=summa))
        summa = summa*SOCIAL_PENSION_INDEX[date_index]
        date_for_period = date_index
    

    if date_index == date(2022, 4, 1):
        date_index = date(2022, 6, 1)
    elif date_index == date(2022, 6, 1):
        date_index = date(2023, 4, 1)
    else: date_index = date(date_index.year+1, 4, 1)

    while date_index < DKpen:

        if isRSD:
            sp_standart_by_year[0].periods.append(PeriodAmount(DN=date_for_period, DK=date_index, amount=summa))

        else:
            sp_standart_by_year[0].periods.append(PeriodAmount(DN=date_for_period, DK=date_index, amount=0))
        
        date_for_period = date_index
        summa = summa*SOCIAL_PENSION_INDEX[date_index]  

        if date_index == date(2022, 4, 1):
            date_index = date(2022, 6, 1)
        elif date_index == date(2022, 6, 1):
            date_index = date(2023, 4, 1)
        else: date_index = date(date_index.year+1, date_index.month, date_index.day) 

    if isRSD:
        sp_standart_by_year[0].periods.append(PeriodAmount(DN=date_for_period, DK=DKpen, amount=summa))
    else:
        sp_standart_by_year[0].periods.append(PeriodAmount(DN=date_for_period, DK=DKpen, amount=0))
    
    return sp_standart_by_year



async def pension_departmental_calculate(pension: PaymentInterface, sp_standart_by_year) -> PaymentsByPeriods:

    """ Функция по расчета стандартных выплат по ведомственной пенсии по годам

    Returns:
        PaymentsByYear: Возвращает словаь с индексом пенсии, которому принадлежит словарь с периодами и соотвествующими стандартными выплатами
    """

    # Начальный период
    DNpen = pension.DN
    DKpen = pension.DK

    sp_standart_by_year[0] = PaymentsByPeriodsItem(
        is_payment_transferred=False,
        is_get_PSD_FSD_last_mounth_payment_trasferred=False,
        is_get_PSD_FSD_last_year_payment_trasferred=False,
        is_Not_get_PSD_FSD_now_payment_trasferred=False,
        type=pension.categoria, 
        periods=[]
    )

    if (pension.is_recalculation and pension.recalculation != None):
        n = len(pension.recalculation)
        # Сортируем пересчеты по дате для надежности
        recalculations = sorted(pension.recalculation, key=lambda x: x.date)
        
        for i in range(n):
            date_rec = recalculations[i].date
            if DNpen < date_rec <= DKpen:
                if i == 0:
                    # Первый пересчет: период от начала до первой даты пересчета
                    sp_standart_by_year[0].periods.append(
                        PeriodAmount(DN=DNpen, DK=date_rec, amount=pension.amount)
                    )
                else:
                    # Период от предыдущей даты пересчета до текущей
                    date_rec_prev = recalculations[i-1].date
                    amount_rec_prev = recalculations[i-1].amount
                    sp_standart_by_year[0].periods.append(
                        PeriodAmount(DN=date_rec_prev, DK=date_rec, amount=amount_rec_prev)
                    )
                
                # Если это последний пересчет, добавляем период до конца
                if i == n - 1:
                    sp_standart_by_year[0].periods.append(
                        PeriodAmount(DN=date_rec, DK=DKpen, amount=recalculations[i].amount)
                    )
    
    return sp_standart_by_year

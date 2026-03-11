from src.constants.payment_const import SOCIAL_PENSION_INDEX, INSURANCE_PENSION_SCORE, INSURANCE_PENSION_FIX_AMOUNT
from datetime import date
from dateutil.relativedelta import relativedelta

from src.utils.payments.types.paymentType import (PaymentsByPeriods, PaymentsByPeriodsItem, PeriodAmount)
from src.schemas.json_query_schema import (
    JsonQuerySchema, PaymentInterface
)

def get_score_fix_amount_insurance(DNpen: date):
    target_score = 0
    target_fix_amount = 0
    
    for current_date, score in INSURANCE_PENSION_SCORE.items():
        if current_date <= DNpen:
            if current_date in INSURANCE_PENSION_FIX_AMOUNT: 
                target_score = score
                target_fix_amount = INSURANCE_PENSION_FIX_AMOUNT[current_date]
        else:
            break

    if target_score == 0:
        print(f"Предупреждение: не найдены значения для даты {DNpen}, чтобы посчитать ИПК")

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
                periods:[{DN, DK, amount}, {DN, DK, amount}]
            };
            1: {
                is_payment_transferred: false
                is_get_PSD_FSD_last_mounth_payment_trasferred: bool
                is_get_PSD_FSD_last_year_payment_trasferred: bool
                is_Not_get_PSD_FSD_now_payment_trasferred: bool
                type: PensionCategoryRaw;
                periods: [{DN, DK, amount},{DN, DK, amount}]
        }
        }
    """    

    pensions = [p for p in data.payments if p.type == 'pension']
    sp_standart_by_year: PaymentsByPeriods = {}

    for pension in pensions:

        if pension.categoria == "insurance_SPK":
            sp_standart_by_year = await pension_insurance_SPK_calculate(pension=pension, sp_standart_by_year=sp_standart_by_year)
        elif pension.categoria == "social_SPK" or pension.categoria == "social_disability":
            sp_standart_by_year = await pension_social_calculate(pension=pension, sp_standart_by_year=sp_standart_by_year)
        elif pension.categoria == "departmental":
            sp_standart_by_year = await pension_departmental_calculate(pension=pension, sp_standart_by_year=sp_standart_by_year)
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

    sp_standart_by_year[pension.id] = PaymentsByPeriodsItem(
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
        return sp_standart_by_year
    

    # Определяем начало периода - всегда 1 января
    if DNpen.month == 1 and DNpen.day == 1:
        # Если уже началось с 1 января
        date_for_period = DNpen
        current_summa = summa
    else:
        # Если началось не с 1 января, создаем первый период с DNpen до 31 декабря
        sp_standart_by_year[pension.id].periods.append(PeriodAmount(
            DN=DNpen,
            DK=date(year, 12, 31),
            amount=summa if isRSD else 0
        ))
        # Следующий период начнется с 1 января следующего года
        date_for_period = date(year + 1, 1, 1)
        # Пересчитываем сумму для следующего года
        current_summa = IPK * INSURANCE_PENSION_SCORE[date(year + 1, 1, 1)] + INSURANCE_PENSION_FIX_AMOUNT[date(year + 1, 1, 1)]
        year += 1

    # Генерируем периоды по годам, начиная с 1 января
    while date_for_period <= DKpen:
        period_end = date(date_for_period.year, 12, 31)
        
        if period_end > DKpen:
            period_end = DKpen
        
        sp_standart_by_year[pension.id].periods.append(PeriodAmount(
            DN=date_for_period,
            DK=period_end,
            amount=current_summa if isRSD else 0
        ))
        
        # Переходим к следующему году
        date_for_period = date(date_for_period.year + 1, 1, 1)
        
        # Пересчитываем сумму для следующего года, если не вышли за пределы
        if date_for_period <= DKpen:
            try:
                current_summa = IPK * INSURANCE_PENSION_SCORE[date(date_for_period.year, 1, 1)] + INSURANCE_PENSION_FIX_AMOUNT[date(date_for_period.year, 1, 1)]
            except KeyError:
                # Если нет данных для следующего года, используем последнее известное значение
                print(f"Предупреждение: нет данных для {date_for_period.year}")

    return sp_standart_by_year



async def pension_social_calculate(pension: PaymentInterface, sp_standart_by_year) -> PaymentsByPeriods:
    """ Функция по расчета стандартных выплат по социальной пенсии по годам """

    DNpen = pension.DN
    DKpen = pension.DK
    summa = pension.amount

    sp_standart_by_year[pension.id] = PaymentsByPeriodsItem(
        is_payment_transferred=pension.is_payment_transferred,
        is_get_PSD_FSD_last_mounth_payment_trasferred=pension.is_get_PSD_FSD_last_mounth_payment_trasferred,
        is_get_PSD_FSD_last_year_payment_trasferred=pension.is_get_PSD_FSD_last_year_payment_trasferred,
        is_Not_get_PSD_FSD_now_payment_trasferred=pension.is_Not_get_PSD_FSD_now_payment_trasferred,
        type=pension.categoria, 
        periods=[]
    )

    isRSD = True
    if pension.is_payment_transferred:
        if not (pension.is_get_PSD_FSD_last_mounth_payment_trasferred and 
                pension.is_get_PSD_FSD_last_year_payment_trasferred and 
                pension.is_Not_get_PSD_FSD_now_payment_trasferred):
            isRSD = False

    # Получаем все даты индексации
    index_dates = sorted(SOCIAL_PENSION_INDEX.keys())
    
    # Находим первую дату индексации в году начала пенсии
    first_idx_in_year = None
    for idx_date in index_dates:
        if idx_date.year == DNpen.year and idx_date >= DNpen:
            first_idx_in_year = idx_date
            break
    
    # Если дата начала не 1 января, создаем период с DNpen до 31 декабря
    if not (DNpen.month == 1 and DNpen.day == 1):
        # Определяем конец первого периода
        if first_idx_in_year and first_idx_in_year > DNpen:
            # Если есть индексация в этом году, период до индексации
            period_end = first_idx_in_year - relativedelta(days=1)
        else:
            # Иначе до конца года
            period_end = date(DNpen.year, 12, 31)
        
        if period_end > DKpen:
            period_end = DKpen
        
        sp_standart_by_year[pension.id].periods.append(PeriodAmount(
            DN=DNpen,
            DK=period_end,
            amount=summa if isRSD else 0
        ))
        
        # Обновляем текущую дату
        if first_idx_in_year and first_idx_in_year <= DKpen:
            current_date = first_idx_in_year
            # Применяем индексацию
            summa = summa * SOCIAL_PENSION_INDEX[first_idx_in_year]
        else:
            current_date = date(DNpen.year + 1, 1, 1)
    else:
        # Если началось с 1 января, начинаем с этой даты
        current_date = DNpen

    # Генерируем последующие периоды по годам
    while current_date <= DKpen:
        # Находим все индексации в текущем году
        indices_in_year = [d for d in index_dates if d.year == current_date.year and d >= current_date]
        
        if indices_in_year:
            # Есть индексации в этом году
            for i, idx_date in enumerate(indices_in_year):
                if idx_date > DKpen:
                    break
                
                # Период до индексации
                if i == 0 and current_date < idx_date:
                    sp_standart_by_year[pension.id].periods.append(PeriodAmount(
                        DN=current_date,
                        DK=idx_date - relativedelta(days=1),
                        amount=summa if isRSD else 0
                    ))
                
                # Период после индексации
                next_date = indices_in_year[i + 1] if i + 1 < len(indices_in_year) else date(current_date.year + 1, 1, 1)
                period_end = min(next_date - relativedelta(days=1), DKpen)
                
                if idx_date <= period_end:
                    sp_standart_by_year[pension.id].periods.append(PeriodAmount(
                        DN=idx_date,
                        DK=period_end,
                        amount=summa if isRSD else 0
                    ))
                    
                    # Применяем следующую индексацию, если она есть
                    if i + 1 < len(indices_in_year):
                        summa = summa * SOCIAL_PENSION_INDEX[indices_in_year[i + 1]]
                
                current_date = period_end + relativedelta(days=1)
        else:
            # Нет индексаций в этом году - весь год одним периодом
            period_end = min(date(current_date.year, 12, 31), DKpen)
            
            sp_standart_by_year[pension.id].periods.append(PeriodAmount(
                DN=current_date,
                DK=period_end,
                amount=summa if isRSD else 0
            ))
            
            current_date = period_end + relativedelta(days=1)
        
        # Если перешли на следующий год, применяем индексацию следующего года
        if current_date.year > current_date.year and current_date <= DKpen:
            next_year_indices = [d for d in index_dates if d.year == current_date.year]
            if next_year_indices:
                summa = summa * SOCIAL_PENSION_INDEX[next_year_indices[0]]

    return sp_standart_by_year



async def pension_departmental_calculate(pension: PaymentInterface, sp_standart_by_year) -> PaymentsByPeriods:
    """ Функция по расчета стандартных выплат по ведомственной пенсии по годам """

    DNpen = pension.DN
    DKpen = pension.DK

    sp_standart_by_year[pension.id] = PaymentsByPeriodsItem(
        is_payment_transferred=pension.is_payment_transferred,
        is_get_PSD_FSD_last_mounth_payment_trasferred=pension.is_get_PSD_FSD_last_mounth_payment_trasferred,
        is_get_PSD_FSD_last_year_payment_trasferred=pension.is_get_PSD_FSD_last_year_payment_trasferred,
        is_Not_get_PSD_FSD_now_payment_trasferred=pension.is_Not_get_PSD_FSD_now_payment_trasferred,
        type=pension.categoria, 
        periods=[]
    )

    if pension.is_recalculation and pension.recalculation:
        # Сортируем перерасчеты по дате
        recalculations = sorted(pension.recalculation, key=lambda x: x.date)
        
        current_date = DNpen
        current_amount = pension.amount
        
        for i, rec in enumerate(recalculations):
            if rec.date <= DNpen:
                continue
            if rec.date > DKpen:
                break
            
            # Период до перерасчета
            if current_date < rec.date:
                # Проверяем, нужно ли разбивать по годам
                while current_date < rec.date:
                    year_end = date(current_date.year, 12, 31)
                    period_end = min(year_end, rec.date - relativedelta(days=1), DKpen)
                    
                    sp_standart_by_year[pension.id].periods.append(PeriodAmount(
                        DN=current_date,
                        DK=period_end,
                        amount=current_amount
                    ))
                    
                    current_date = period_end + relativedelta(days=1)
                    
                    if current_date >= rec.date:
                        break
            
            # Применяем перерасчет
            current_amount = rec.amount
            current_date = rec.date
        
        # Последний период после всех перерасчетов
        if current_date <= DKpen:
            while current_date <= DKpen:
                year_end = date(current_date.year, 12, 31)
                period_end = min(year_end, DKpen)
                
                sp_standart_by_year[pension.id].periods.append(PeriodAmount(
                    DN=current_date,
                    DK=period_end,
                    amount=current_amount
                ))
                
                current_date = period_end + relativedelta(days=1)
    else:
        # Без перерасчетов - разбиваем по годам
        current_date = DNpen
        while current_date <= DKpen:
            year_end = date(current_date.year, 12, 31)
            period_end = min(year_end, DKpen)
            
            sp_standart_by_year[pension.id].periods.append(PeriodAmount(
                DN=current_date,
                DK=period_end,
                amount=pension.amount
            ))
            
            current_date = period_end + relativedelta(days=1)
    
    return sp_standart_by_year





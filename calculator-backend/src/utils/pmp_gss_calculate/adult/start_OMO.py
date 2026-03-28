from src.schemas.json_query_schema import JsonQuerySchema,PaymentInterface
from src.constants.payment_const import (
    INSURANCE_PENSION_SCORE, SOCIAL_PENSION_INDEX, INSURANCE_PENSION_INDEX
)
from datetime import date, timedelta

#ищет пенсии
def find_pension(query:JsonQuerySchema):
    penssii = {}
    flag = 0
    for i in query.payments:
        if i.type == "pension":
            penssii[flag] = i
            flag += 1
        else:
            continue # тут дописать развилку для egdv и так далее
    return penssii

#ищет пенсии в Москве
def get_pensions_in_Moscow(penssii: dict, query: JsonQuerySchema):
    pensii_in_Moscow = {}
    flag = 0

    for i in penssii.values():
        if i.is_Moscow:

            DN = i.DN
            DK = i.DK

            if query.change_last_date <= DN < DK:
                i.DN = DN
                i.DK = DK
            else:
                if DN < query.change_last_date < DK:
                    i.DN = query.change_last_date
                    i.DK = DK

            pensii_in_Moscow[flag] = i
            flag += 1
    return pensii_in_Moscow

#счётчик дат перерасчёта дат социальной или государственной пенсии
def social_or_gosudarstvennaya_pereraschet(pension: PaymentInterface):
    DN = pension.DN
    DK = pension.DK

    current_amount = pension.amount
    current_start = DN

    periods_pereraschet = {}
    period_index = 0

    if not pension.recalculation: 
        periods_pereraschet[period_index] = {
            "DN": DN,
            "DK": DK,
            "amount": current_amount
        }
        # pension.periods_pereraschet = periods_pereraschet
        return periods_pereraschet

    recalculation_sorted = sorted(pension.recalculation, key=lambda x: x.date)

    for rec in recalculation_sorted:
        rec_date = rec.date
        rec_amount = rec.amount

        if rec_date <= DN or rec_date >= DK:
            continue

        periods_pereraschet[period_index] = {
            "DN": current_start,
            "DK": rec_date,
            "amount": current_amount
        }
        period_index += 1

        current_start = rec_date
        current_amount = rec_amount

    if current_start < DK:
        periods_pereraschet[period_index] = {
            "DN": current_start,
            "DK": DK,
            "amount": current_amount
        }

    # pension.periods_pereraschet = periods_pereraschet
    return periods_pereraschet

#индексация по периодам социальной или государственной пенсии
def social_or_gosudarstvennaya_indexation(pension: PaymentInterface):
    periods_indexation = {}
    flag = 0
    periods_pereraschet = social_or_gosudarstvennaya_pereraschet(pension)
    for index, period in periods_pereraschet.items():
        dn = period["DN"]
        dk = period["DK"]
        amount = period["amount"]
        date_indexation = date(dn.year + 0, 4, 1)

        if dn > date_indexation:
            if index != 0 :
                data = dn
                sum = amount
            else:
                if pension.is_payment_transferred:
                    #проверяем последний месяц и год
                    if pension.is_get_PSD_FSD_last_mounth_payment_trasferred and pension.is_get_PSD_FSD_last_year_payment_trasferred:
                        #проверяем прекращена ли РСД
                        if not pension.is_Not_get_PSD_FSD_now_payment_trasferred:
                            periods_indexation[flag] = {
                                "DN": None,
                                "DK": None,
                                "amount": None
                            }
                            break
                        else:
                            amount_latest = amount / SOCIAL_PENSION_INDEX[date_indexation]
                            periods_indexation[flag] = {
                                "DN": date(date_indexation.year - 1, 4, 1),
                                "DK": date_indexation,
                                "amount": amount_latest
                            }
                            flag += 1
                            data = dn
                            date_indexation=date(date_indexation.year + 1, 4, 1)
                            sum=amount
                    else:
                        data = dn
                        sum = amount
                        date_indexation=date(date_indexation.year + 1, 4, 1)
                else:
                    data = dn
                    sum = amount
                    date_indexation=date(date_indexation.year + 1, 4, 1)
        else:
            data = dn
            date_indexation=date_indexation
            sum=amount
            
        while date_indexation < dk:
            periods_indexation[flag] = {
                "DN": data,
                "DK": date_indexation,
                "amount": sum
            }
            flag += 1

            data = date_indexation
            sum = sum * SOCIAL_PENSION_INDEX[date_indexation]

            if date_indexation == date(2022, 4, 1):
                date_indexation = date(2022, 6, 1)
            elif date_indexation == date(2022, 6, 1):
                ndate_indexation = date(2023, 4, 1)
            else:
                date_indexation = date(date_indexation.year + 1, 4, 1)

        periods_indexation[flag] = {
            "DN": data,
            "DK": dk,
            "amount": sum
        }
        flag += 1

    # pension.period_pensii = periods_indexation
    return periods_indexation

#ветка ведомственная или другая или месячная выплата
def get_period_pensii_other_categories(payment: PaymentInterface) -> dict:
    period_pensii = {}

    # Ветка для vedomostvennaya / other
    if payment.categoria in ("departmental", "other"):
        DN = payment.DN if payment.DN is not None else payment.periods[0]
        DK = payment.DK if payment.DK is not None else payment.periods[1]

        current_amount = float(payment.amount)
        current_start = DN
        period_index = 0

        # Если перерасчетов нет — один период
        if not payment.recalculation:
            period_pensii[period_index] = {
                "DN": DN,
                "DK": DK,
                "amount": current_amount
            }
            return period_pensii

        # Сортируем перерасчеты по дате
        recalculation_sorted = sorted(payment.recalculation, key=lambda x: x.date)

        # Разбиваем период по датам перерасчета
        for rec in recalculation_sorted:
            rec_date = rec.date
            rec_amount = float(rec.amount)

            # Берем только перерасчеты внутри периода
            if rec_date <= DN or rec_date >= DK:
                continue

            period_pensii[period_index] = {
                "DN": current_start,
                "DK": rec_date,
                "amount": current_amount
            }
            period_index += 1

            current_start = rec_date
            current_amount = rec_amount

        # Последний период
        if current_start < DK:
            period_pensii[period_index] = {
                "DN": current_start,
                "DK": DK,
                "amount": current_amount
            }

        return period_pensii

    # Ветка для monthPay
    if payment.categoria == "monthPay":
        DN = payment.DN if payment.DN is not None else payment.periods[0]
        DK = payment.DK if payment.DK is not None else payment.periods[1]

        period_pensii[0] = {
            "DN": DN,
            "DK": DK,
            "amount": float(payment.amount)
        }
        return period_pensii

#счётчик дат перерасчёта дат страховой с фиксированной выплатой
def fix_insurance_recalculation(pension: PaymentInterface):
    periods_pereraschet = {}

    if pension.is_recalculation_fix_amount:
        DN = pension.DN
        DK = pension.DK

        final_DK = DK
        current_start = DN
        current_amount = pension.amount_fix
        period_index = 0

        recalculation_sorted = sorted(pension.recalculation_fix_amount, key=lambda x: x.date)

        for rec in recalculation_sorted:
            rec_date = rec.date
            rec_amount = rec.amount

            if current_start < rec_date < final_DK:
                periods_pereraschet[period_index] = {
                    "DN": current_start,
                    "DK": rec_date,
                    "amount": current_amount
                    }
                period_index += 1

                current_start = rec_date
                current_amount = rec_amount
            else:
                continue

        periods_pereraschet[period_index] = {
            "DN": current_start,
            "DK": final_DK,
            "amount": current_amount
        }

    else:
        periods_pereraschet[0] = {
            "DN": pension.DN,
            "DK": pension.DK,
            "amount": pension.amount_fix
        }

        # pension.periods_pereraschet = periods_pereraschet
    return periods_pereraschet


#индексация по периодам страховой с фиксированной выплатой
def fix_insurance_indexation(pension: PaymentInterface):
    items = list(INSURANCE_PENSION_INDEX.items())
    j = 0
    periods_indexation = {}
    periods_pereraschet = fix_insurance_recalculation(pension)
    
    date_indexation = None

    # 1. спецобработка только нулевого периода
    dn0 = periods_pereraschet[0]["DN"]

    if dn0 != date(dn0.year, 12, 31):
        if pension.is_payment_transferred:
            if (
                pension.is_get_PSD_FSD_last_mounth_payment_trasferred
                and pension.is_get_PSD_FSD_last_year_payment_trasferred
            ):
                if not pension.is_Not_get_PSD_FSD_now_payment_trasferred:
                    periods_indexation[j] = {
                        "DN": None,
                        "DK": None,
                        "amount": None
                    }
                    # pension.result_fix = periods_indexation
                    return periods_indexation
                else:
                    found = False
                    fix_amount = 0
                    date_indexation = None

                    for i in range(len(items) - 1):
                        d1, value1 = items[i]
                        d2, value2 = items[i + 1]

                        if d1 <= dn0 < d2:
                            d_last, value_last = items[i]
                            fix_amount = (
                                periods_pereraschet[0]["amount"]
                                / INSURANCE_PENSION_INDEX[d_last]
                            )
                            date_indexation = date(d_last.year - 1, 12, 1)
                            found = True
                            break

                    if not found:
                        fix_amount = 0
                        date_indexation = None

                    periods_indexation[j] = {
                        "DN": date_indexation,
                        "DK": dn0,
                        "amount": fix_amount
                    }
                    j += 1

    # 2. дальше идем по всем периодам перерасчета
    for period in periods_pereraschet.values():
        dn = period["DN"]
        dk = period["DK"]
        summa = period["amount"]

        D = date(dn.year + 1, 1, 1)

        while D < dk:
            periods_indexation[j] = {
                "DN": dn,
                "DK": D,
                "amount": summa
            }
            j += 1
            dn = D

            found = False
            for i in range(len(items) - 1):
                d1, value1 = items[i]
                d2, value2 = items[i + 1]

                if d1 <= D < d2:
                    summa = summa * INSURANCE_PENSION_INDEX[d1]
                    found = True
                    break

            if not found:
                last_date = items[-1][0]
                if D >= last_date:
                    summa = summa * INSURANCE_PENSION_INDEX[last_date]
                else:
                    summa = 0

            D = date(D.year + 1, 1, 1)

        periods_indexation[j] = {
            "DN": dn,
            "DK": dk,
            "amount": summa
        }
        j += 1

    # pension.result_fix = periods_indexation
    return periods_indexation

#ветка страховая с перерасчётом и без перерасчета
def get_pensii_yes_recalculation(pension: PaymentInterface):
    pensii_itog_res = {}
    ipk_items = list(INSURANCE_PENSION_SCORE.items())

    def get_ipk_cost_by_date(target_date: date):
        for idx in range(len(ipk_items) - 1):
            d1, ipk_cost = ipk_items[idx]
            d2, _ = ipk_items[idx + 1]
            if d1 <= target_date < d2:
                return ipk_cost

        return None

    def get_prev_ipk_cost_by_date(target_date: date):
        for idx in range(len(ipk_items) - 1):
            d1, ipk_cost = ipk_items[idx]
            d2, _ = ipk_items[idx + 1]
            if d1 <= target_date < d2:
                if idx > 0:
                    return ipk_items[idx - 1][1]
                return ipk_cost

        return ipk_items[-1][1]

    if not pension.is_recalculation or pension.recalculation is None:
        date_start = pension.DN
        date=pension.DK
        amount = pension.amount
        periods[0] = {
                "DN": date_start, 
                "DK":date,
                "amount": amount    
            }

    else:
        pension.recalculation.sort(key=lambda rec: rec.date)

            # ==========================================================
            # 1. Формируем периоды по датам перерасчета
            # ==========================================================
        periods = {}
        period_index = 0

        date_start = pension.DN
        amount = pension.amount

        for rec in pension.recalculation:
            if pension.DN <= rec.date <= pension.DK:
                periods[period_index] = {
                    "DN": date_start,  # заменили "start_date" на "DN"
                    "DK": rec.date,    # заменили "end_date" на "DK"
                    "amount": amount    # заменили "summa" на "amount"
                }
                date_start = rec.date
                amount = rec.amount
                period_index += 1

        periods[period_index] = {
            "DN": date_start,  # заменили "start_date" на "DN"
            "DK": pension.DK,  # заменили "end_date" на "DK"
            "amount": amount    # заменили "summa" на "amount"
        }

        # ==========================================================
        # 2. Считаем ИПК для каждого периода перерасчета
        # ==========================================================
    periods_ipk = {}

    for j, period in periods.items():
        date_start_period = period["DN"]
        amount_period = period["amount"]

        ipk_cost = get_ipk_cost_by_date(date_start_period)
        if ipk_cost is not None:
            periods_ipk[j] = {
                "DN": date_start_period,  # заменили "start_date" на "DN"
                "DK": period["DK"],      # заменили "end_date" на "DK"
                "ipk": amount_period / ipk_cost
            }

        # ==========================================================
        # 3. Формируем итоговые периоды с ежегодной индексацией
        # ==========================================================
    periods_final = {}
    final_index = 0

        # ----------------------------------------------------------
        # 3.0. Специальный первый период: с 01.01 года до DN
        # Логика с переводом пенсии применяется ТОЛЬКО здесь
        # ----------------------------------------------------------
    start_of_year = date(pension.DN.year, 1, 1)

    if pension.DN > start_of_year:
        if pension.is_payment_transferred:
            if (
                pension.is_get_PSD_FSD_last_mounth_payment_trasferred
                and pension.is_get_PSD_FSD_last_year_payment_trasferred
            ):
                if not pension.is_Not_get_PSD_FSD_now_payment_trasferred:
                    first_amount = 0.0
                else:
                    current_cost = get_ipk_cost_by_date(pension.DN)
                    prev_cost = get_prev_ipk_cost_by_date(pension.DN)

                    first_ipk = pension.amount / current_cost
                    first_amount = first_ipk * prev_cost
            else:
                first_amount = pension.amount

                periods_final[final_index] = {
                    "DN":date(start_of_year.year - 1, 12, 1),
                    "DK": pension.DN,     # заменили "end_date" на "DK"
                    "amount": round(first_amount, 2)  # заменили "summa" на "amount"
                }
                final_index += 1

        # ----------------------------------------------------------
        # 3.1. Реальные периоды перерасчета
        # Главное правило:
        # если дата совпадает с пользовательской датой периода,
        # оставляем исходную сумму пользователя,
        # а через ИПК считаем только после 1 января
        # ----------------------------------------------------------
    for j, period_ipk in periods_ipk.items():
        date_start_j = period_ipk["DN"]
        date_end_j = period_ipk["DK"]
        ipk = period_ipk["ipk"]

        current_start = date_start_j

            # ВАЖНО:
            # первый кусок каждого пользовательского периода
            # всегда идет с исходной суммой пользователя
        current_amount = periods[j]["amount"]

        while True:
            next_index_date = date(current_start.year + 1, 1, 1)

                # Если 1 января лежит внутри текущего периода,
                # то до него сохраняем исходную сумму пользователя
            if next_index_date < date_end_j:
                periods_final[final_index] = {
                    "DN": current_start,  # заменили "start_date" на "DN"
                    "DK": next_index_date,  # заменили "end_date" на "DK"
                    "amount": round(current_amount, 2)  # заменили "summa" на "amount"
                }
                final_index += 1

                    # После 1 января уже начинаем считать через ИПК
                current_start = next_index_date
                new_ipk_cost = get_ipk_cost_by_date(current_start)

                if new_ipk_cost is not None:
                    current_amount = ipk * new_ipk_cost
            else:
                    # Если период не дошел до следующего 1 января,
                    # оставляем исходную сумму без пересчета через ИПК
                periods_final[final_index] = {
                    "DN": current_start,  # заменили "start_date" на "DN"
                    "DK": date_end_j,     # заменили "end_date" на "DK"
                    "amount": round(current_amount, 2)  # заменили "summa" на "amount"
                }
                final_index += 1
                break

        # Итоговые данные без ключей "type" и "periods"
        pensii_itog_res = periods_final

    return pensii_itog_res


#схлапывание страховой пенсий с перерасчётом и без него
def fixed_payment_and_insurance_pension(
    res_insurance_part: dict,
    result_fix: dict
):
    result_pensii = {}
    new_index = 0

    # Проходим по каждому периоду страховки
    for insurance_period in res_insurance_part.values():
        # Каждый insurance_period уже является словарем с ключами DN, DK, amount
        date_start_insurance_j = insurance_period["DN"]
        date_end_insurance_j = insurance_period["DK"]
        insurance_summa_j = insurance_period["amount"]

        # Проходим по каждому фиксированному периоду
        for fix_period in result_fix.values():
            # Каждый fix_period также является словарем с ключами DN, DK, amount
            date_start_fix_d = fix_period["DN"]
            date_end_fix_d = fix_period["DK"]
            fix_summa_d = fix_period["amount"]

            # Логика перерасчёта: вычисление итоговой суммы для пересекающихся периодов
            if date_start_insurance_j <= date_start_fix_d < date_end_insurance_j <= date_end_fix_d:
                summ_itog = insurance_summa_j + fix_summa_d
                result_pensii[new_index] = {
                    "DN": date_start_fix_d,  # Используем "DN" вместо "date_start"
                    "DK": date_end_insurance_j,  # Используем "DK" вместо "date_end"
                    "amount": summ_itog  # Используем "amount" вместо "summa"
                }
                new_index += 1

            elif date_start_fix_d <= date_start_insurance_j < date_end_fix_d <= date_end_insurance_j:
                summ_itog = insurance_summa_j + fix_summa_d
                result_pensii[new_index] = {
                    "DN": date_start_insurance_j,  # Используем "DN" вместо "date_start"
                    "DK": date_end_fix_d,  # Используем "DK" вместо "end_date"
                    "amount": summ_itog  # Используем "amount" вместо "summa"
                }
                new_index += 1

            elif date_start_fix_d <= date_start_insurance_j < date_end_insurance_j <= date_end_fix_d:
                summ_itog = insurance_summa_j + fix_summa_d
                result_pensii[new_index] = {
                    "DN": date_start_insurance_j,  # Используем "DN" вместо "start_date"
                    "DK": date_end_insurance_j,  # Используем "DK" вместо "end_date"
                    "amount": summ_itog  # Используем "amount" вместо "summa"
                }
                new_index += 1

            elif date_start_insurance_j <= date_start_fix_d < date_end_fix_d <= date_end_insurance_j:
                summ_itog = insurance_summa_j + fix_summa_d
                result_pensii[new_index] = {
                    "DN": date_start_fix_d,  # Используем "DN" вместо "start_date"
                    "DK": date_end_fix_d,  # Используем "DK" вместо "end_date"
                    "amount": summ_itog  # Используем "amount" вместо "summa"
                }
                new_index += 1

            else:
                continue

    # Сортировка результатов по дате начала периода
    sorted_periods = sorted(
        result_pensii.values(),
        key=lambda x: x["DN"]  # Сортируем по "DN"
    )

    # Индексируем отсортированные периоды
    result_pensii_sorted = {i: period for i, period in enumerate(sorted_periods)}

    return result_pensii_sorted




def pensii_devochki(query: JsonQuerySchema):
    '''
    Возвращает данные формата:
    {
        0: {
            'type': 'insurance', 
            'is_payment_transferred': bool,
            'is_get_PSD_FSD_last_mounth_payment_trasferred': bool,
            'is_get_PSD_FSD_last_year_payment_trasferred': bool,
            'is_Not_get_PSD_FSD_now_payment_trasferred': bool,
            'periods': {
                0: {'DN': date, 'DK': date, 'amount': float}, ...
            }
        }, ...
    }
    '''
    
    pensii = find_pension(query)
    pensii_in_Moscow = get_pensions_in_Moscow(pensii, query)

    result = {}
    pensiya_counter = 0

    for pension in pensii_in_Moscow.values():
        pensiya_key = pensiya_counter
        pensiya_counter += 1

        base_result = {
            'type': pension.categoria,
            'is_payment_transferred': pension.is_payment_transferred,
            'is_get_PSD_FSD_last_mounth_payment_trasferred': pension.is_get_PSD_FSD_last_mounth_payment_trasferred,
            'is_get_PSD_FSD_last_year_payment_trasferred': pension.is_get_PSD_FSD_last_year_payment_trasferred,
            'is_Not_get_PSD_FSD_now_payment_trasferred': pension.is_Not_get_PSD_FSD_now_payment_trasferred,
        }

        # Обработка по категориям
        if pension.categoria == "insurance":
            # Получаем страховую часть
            insurance_periods = get_pensii_yes_recalculation(pension)  # Только pension!
            
            # Если есть фиксированная часть
            if pension.is_fix_amount:
                fix_periods = fix_insurance_recalculation(pension)
                fix_indexed = fix_insurance_indexation(pension)  # Передаем pension, не словарь!
                
                # Объединяем
                base_result['periods'] = fixed_payment_and_insurance_pension(
                    insurance_periods,  # Страховая часть
                    fix_indexed         # Фиксированная часть с индексацией
                )
            else:
                base_result['periods'] = insurance_periods

        elif pension.categoria in ("social", "gosudarstvennaya"):
            periods = social_or_gosudarstvennaya_pereraschet(pension)
            indexed_periods = social_or_gosudarstvennaya_indexation(pension)  # Передаем pension!
            base_result['periods'] = indexed_periods

        elif pension.categoria in ("other", "monthPay", "departmental"):
            base_result['periods'] = get_period_pensii_other_categories(pension)

        else:
            continue

        result[pensiya_key] = base_result

    return result
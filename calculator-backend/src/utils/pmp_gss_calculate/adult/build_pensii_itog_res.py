from datetime import date, datetime


from src.schemas.json_query_schema import JsonQuerySchema, PaymentInterface
from src.utils.payments.types.paymentType import PeriodAmount




def _build_pensii_itog_res(
    sorted_pensions: dict,
    edk: dict = None,
    edv: dict = None,
    egdv: dict = None,
    housing: dict = None,
) -> dict:
    """
    Собирает pensii_itog_res из всех потоков выплат для передачи в calculate_pension_itog.
    Конвертирует DN/DK/amount → date_start/date_end/summa.
    """
    pensii_itog_res: dict = {}

    # # ПМП / ГСС периоды из sorted_pensions (dict с полями DN, DK, amount)
    # for pension_id, periods in sorted_pensions.items():
    #     pensii_itog_res[f"pmp_gss_{pension_id}"] = {
    #         "periods": {
    #             i: {"date_start": p.DN, "date_end": p.DK, "summa": p.amount}
    #             for i, p in enumerate(periods)
    #         }
    #     }
    
    # ПМП / ГСС периоды из sorted_pensions
    for pension_id, pension_data in sorted_pensions.items():
        if isinstance(pension_data, dict) and 'periods' in pension_data:
            periods_dict = pension_data['periods']
            pensii_itog_res[f"pension_{pension_id}"] = {
                "periods": {
                    i: {
                        "date_start": period['DN'],
                        "date_end": period['DK'],
                        "summa": period['amount']
                    }
                    for i, period in periods_dict.items()
                },
                "transferred": {
                    "is_payment_transferred": pension_data.get('is_payment_transferred'),
                    "is_get_PSD_FSD_last_mounth_payment_trasferred": pension_data.get('is_get_PSD_FSD_last_mounth_payment_trasferred'),
                    "is_get_PSD_FSD_last_year_payment_trasferred": pension_data.get('is_get_PSD_FSD_last_year_payment_trasferred'),
                    "is_Not_get_PSD_FSD_now_payment_trasferred": pension_data.get('is_Not_get_PSD_FSD_now_payment_trasferred')
                }
            }
        else:
            print(f"Неожиданная структура для pension_id {pension_id}: {type(pension_data)}")
            continue

    # ЕДК (edk)
    if edk is not None:
        for payment_id, periods in edk.items():
            pensii_itog_res[f"edk_{payment_id}"] = {
                "periods": {
                    i: {"date_start": p.DN, "date_end": p.DK, "summa": p.amount}
                    for i, p in enumerate(periods)
                }
            }

    # ЕДВ / НСУ
    if edv is not None:
        for payment_id, periods in edv.items():
            pensii_itog_res[f"edv_{payment_id}"] = {
                "periods": {
                    i: {"date_start": p.DN, "date_end": p.DK, "summa": p.amount}
                    for i, p in enumerate(periods)
                }
            }

    # ЕГДВ
    if egdv is not None:
        for payment_id, periods in egdv.items():
            pensii_itog_res[f"egdv_{payment_id}"] = {
                "periods": {
                    i: {"date_start": p.DN, "date_end": p.DK, "summa": p.amount}
                    for i, p in enumerate(periods)
                }
            }

    # ЖКУ (housing)
    if housing is not None:
        for payment_id, periods in housing.items():
            pensii_itog_res[f"housing_{payment_id}"] = {
                "periods": {
                    i: {"date_start": p.DN, "date_end": p.DK, "summa": p.amount}
                    for i, p in enumerate(periods)
                }
            }

    return pensii_itog_res



if __name__ == "__main__":
    # ИСПРАВЛЕНО: Используем date() вместо datetime.date()
    edv_result = {
        0: [
            PeriodAmount(DN=date(2024, 7, 1), DK=date(2025, 2, 1), amount=15200.0),
            PeriodAmount(DN=date(2025, 2, 1), DK=date(2025, 7, 1), amount=16644.0)
        ],
        1: [
            PeriodAmount(DN=date(2025, 7, 1), DK=date(2026, 2, 1), amount=17800.0),
            PeriodAmount(DN=date(2026, 2, 1), DK=date(2026, 3, 1), amount=18796.8)
        ]
    }
    
    edk_result = {
        0: [
            PeriodAmount(DN=date(2024, 7, 1), DK=date(2025, 1, 1), amount=2654.0),
            PeriodAmount(DN=date(2025, 1, 1), DK=date(2025, 7, 1), amount=2818.06)
        ],
        1: [
            PeriodAmount(DN=date(2025, 7, 1), DK=date(2026, 1, 1), amount=2831.25),
            PeriodAmount(DN=date(2026, 1, 1), DK=date(2026, 3, 1), amount=2831.25)
        ]
    }
    
    egdv_result = {
        0: [
            PeriodAmount(DN=date(2024, 7, 1), DK=date(2025, 1, 1), amount=2654.0),
            PeriodAmount(DN=date(2025, 1, 1), DK=date(2025, 7, 1), amount=2818.06)
        ],
        1: [
            PeriodAmount(DN=date(2025, 7, 1), DK=date(2026, 1, 1), amount=2831.25),
            PeriodAmount(DN=date(2026, 1, 1), DK=date(2026, 3, 1), amount=2831.25)
        ]
    }
    
    housin_result = {
        0: [
            PeriodAmount(DN=date(2024, 7, 1), DK=date(2025, 2, 1), amount=15200.0),
            PeriodAmount(DN=date(2025, 2, 1), DK=date(2025, 7, 1), amount=16644.0)
        ],
        1: [
            PeriodAmount(DN=date(2025, 7, 1), DK=date(2026, 2, 1), amount=17800.0),
            PeriodAmount(DN=date(2026, 2, 1), DK=date(2026, 3, 1), amount=18796.8)
        ]
    }
    
    # Добавляем sorted_pensions (пустой словарь, так как он не используется в тесте)
    sorted_pensions = {}
    
    pensii_itog_res = _build_pensii_itog_res(
        sorted_pensions=sorted_pensions,  # Добавлен недостающий аргумент
        edk=edk_result,
        edv=edv_result,
        egdv=egdv_result,
        housing=housin_result,
    )

    print(pensii_itog_res)

    
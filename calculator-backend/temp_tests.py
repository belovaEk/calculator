from datetime import date
from src.utils.payments.pension_summary import calculate_pension_itog


pensions_result = {0: {'type': 'insurance', 'periods': {0: {'DN': date(2022, 2, 1), 'DK': date(2023, 1, 1), 'amount': 4000.0}, 1: {'DN': date(2023, 1, 1), 'DK': date(2024, 1, 1), 'amount': 4611.4}, 2: {'DN': date(2024, 1, 1), 'DK': date(2025, 1, 1), 'amount': 4957.15}, 3: {'DN': date(2025, 1, 1), 'DK': date(2026, 1, 1), 'amount': 5428.09}, 4: {'DN': date(2026, 1, 1), 'DK': date(2026, 3, 6), 'amount': 5840.54}}}}
pension_itog = calculate_pension_itog(pensions_result)
print(pension_itog)
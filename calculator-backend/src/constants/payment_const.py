from typing import  Dict
from datetime import date

INSURANCE_PENSION_SCORE: Dict[date, float] = {
    date(2020, 1, 1): 93.00,
    date(2021, 1, 1): 98.86,
    date(2022, 1, 1): 107.36,
    date(2022, 6, 1): 118.10,
    date(2023, 1, 1): 123.77,
    date(2024, 1, 1): 133.05,
    date(2025, 1, 1): 145.69,
    date(2026, 1, 1): 156.76,
}

INSURANCE_PENSION_FIX_AMOUNT: Dict[date, float] = {
    date(2020, 1, 1): 5686.25,
    date(2021, 1, 1): 6044.48,
    date(2022, 1, 1): 6564.31,
    date(2022, 6, 1): 7220.74,
    date(2023, 1, 1): 7567.33,
    date(2024, 1, 1): 8134.88,
    date(2025, 1, 1): 8907.70,
    date(2026, 1, 1): 9584.69,
}


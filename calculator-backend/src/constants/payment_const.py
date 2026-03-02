from typing import  Dict
from datetime import date

INSURANCE_PENSION_SCORE: Dict[date, float] = {
    date(2020, 01, 01): 93.00,
    date(2021, 01, 01): 98.86,
    date(2022, 01, 01): 107.36,
    date(2022, 06, 01): 118.10,
    date(2023, 01, 01): 123.77,
    date(2024, 01, 01): 133.05,
    date(2025, 01, 01): 145.69,
    date(2026, 01, 01): 156.76,
}

INSURANCE_PENSION_FIX_AMOUNT: Dict[date, float] = {
    date(2020, 01, 01): 5686.25,
    date(2021, 01, 01): 6044.48,
    date(2022, 01, 01): 6564.31,
    date(2022, 06, 01): 7220.74,
    date(2023, 01, 01): 7567.33,
    date(2024, 01, 01): 8134.88,
    date(2025, 01, 01): 8907.70,
    date(2026, 01, 01): 9584.69,
}


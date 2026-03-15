from typing import  Dict
from datetime import date

EDK_KIND: Dict[date, float] = {
    date(2023, 1, 1): 1,
    date(2024, 1, 1): 1.041667,
    date(2025, 1, 1): 1.061818,
    date(2026, 1, 1): 1,
}

EDV_INDEX: Dict[date, float] = {
    date(2017, 2, 1): 1.054,
    date(2018, 2, 1): 1.025,
    date(2019, 2, 1): 1.043,
    date(2020, 2, 1): 1.03,
    date(2021, 2, 1): 1.049,
    date(2022, 2, 1): 1.084,
    date(2023, 2, 1): 1.119,
    date(2024, 2, 1): 1.074,
    date(2025, 2, 1): 1.095,
    date(2026, 2, 1): 1.056,
}

EGDV_AMOUNTS: Dict[date, Dict[str, float]] = {
    date(2022, 1, 1): {"reabilitirovan": 2297, "truzhennik": 1722, "war_child": 1722, "labor_veteran": 1149, "labor_veteran_55_60": 1149},
    date(2023, 1, 1): {"reabilitirovan": 2527, "truzhennik": 1895, "war_child": 1895, "labor_veteran": 1264, "labor_veteran_55_60": 1264},
    date(2024, 1, 1): {"reabilitirovan": 2654, "truzhennik": 1990, "war_child": 1990, "labor_veteran": 1328, "labor_veteran_55_60": 1328},
    date(2025, 1, 1): {"reabilitirovan": 2800, "truzhennik": 2100, "war_child": 2100, "labor_veteran": 1328, "labor_veteran_55_60": 1328},
    date(2026, 1, 1): {"reabilitirovan": 2968, "truzhennik": 2226, "war_child": 2226, "labor_veteran": 1328, "labor_veteran_55_60": 1328},
}

HOUSIN_AMOUNTS: Dict[date, float] = {
    date(2019, 1, 1): 1530.53,
    date(2019, 7, 1): 1579.02,
    date(2020, 1, 1): 1591.50,
    date(2020, 7, 1): 1638.36,
    date(2021, 1, 1): 1652.35,
    date(2021, 7, 1): 1696.84,
    date(2022, 1, 1): 1777.19,
    date(2022, 7, 1): 1859.92,
    date(2022, 12, 1): 1991.74,
    date(2023, 1, 1): 2114.95,
    date(2024, 1, 1): 2236.26,
    date(2024, 7, 1): 2431.07,
    date(2025, 1, 1): 2573.99,
    date(2025, 7, 1): 2831.25,
    date(2026, 1, 1): 2958.80,
}

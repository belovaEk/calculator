from typing import List
from src.schemas.json_query_schema import PeriodType

async def transformation_gss_to_pmp(gss_periods: List[PeriodType], pmp_periods: List[PeriodType]):
    new_pmp_periods = gss_periods + pmp_periods

    return {
        "pmp_periods": new_pmp_periods,
        "gss_periods": []
    }

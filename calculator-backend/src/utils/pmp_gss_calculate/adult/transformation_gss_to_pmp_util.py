from typing import List
from src.schemas.json_query_schema import PeriodType

from src.utils.pmp_gss_calculate.common.merge_periods_util import merge_periods

async def transformation_gss_to_pmp(gss_periods: List[PeriodType], pmp_periods: List[PeriodType]):
    new_pmp_periods: List[PeriodType] = gss_periods + pmp_periods
    
    merged_periods = merge_periods(new_pmp_periods)

    return {
        "pmp_periods": merged_periods,
        "gss_periods": []
    }

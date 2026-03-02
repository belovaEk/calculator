from typing import List, Dict, TypeAlias
from datetime import date
from src.schemas.json_query_schema import PeriodType


GssPmpPensionType: TypeAlias = Dict[int, List[PeriodType]]

GssPmpIndexType: TypeAlias = Dict[int, List[date]]
from src.utils.pmp_gss_calculate.type import GssPmpPensionType


from src.utils.pmp_gss_calculate.common.recalculation_date_index_util import recalculation_date_index

async def pmp_date_index (pmp_periods: GssPmpPensionType):

    """Функция пересчета ПМП и ГСС на периоды индексации
    """   
    
    new_pmp_periods = recalculation_date_index(pensions=pmp_periods)

    return {
        'pmp_periods': new_pmp_periods,
    }

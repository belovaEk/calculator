from typing import Dict, Any

PeriodDict = Dict[int, Dict[str, Any]]

def calculate_pension_itog(pensii_itog_res: dict) -> dict:
    if not pensii_itog_res:
        return {}
    
    all_periods = [
        period
        for pension in pensii_itog_res.values()
        for period in pension['periods'].values()
    ]
    print("=" * 80)
    print(all_periods)

    if not all_periods:
        return {}

    breakpoints = sorted({
        d
        for p in all_periods
        for d in (p['date_start'], p['date_end'])
    })
    print("=" * 80, "breakpoints")

    print(breakpoints)
    result: dict = {}
    idx = 0

    for i in range(len(breakpoints) - 1):
        ds = breakpoints[i]
        de = breakpoints[i + 1]

        total: float = sum(
            p['summa']
            for p in all_periods
            if p['date_start'] <= ds < p['date_end']
        )
        print("=" * 80, "total")

        print(total)
        if total > 0:
            result[idx] = {'date_start': ds, 'date_end': de, 'summa': total}
            idx += 1
        
        print("=" * 80, "result")

        print(result)

    return dict(sorted(result.items(), key=lambda kv: kv[1]['date_start']))
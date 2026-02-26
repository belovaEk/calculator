export type periodType = 'регистрация' | 'пребывание в стационаре';

export const PERIOD_TYPE: Record<string, periodType> = {
    registration: 'регистрация',
    inpatient: 'пребывание в стационаре'
}
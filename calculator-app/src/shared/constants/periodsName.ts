export type PeriodType = 'регистрация' | 'пребывание в стационаре' | 'приостановление выплаты';

export const PERIOD_TYPE: Record<string, PeriodType> = {
    registration: 'регистрация',
    inpatient: 'пребывание в стационаре',
    stop_payment: 'приостановление выплаты',
}
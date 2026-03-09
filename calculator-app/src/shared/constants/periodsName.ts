export type PeriodType = 'регистрация' | 'пребывание в стационаре' | 'приостановление выплаты' | 'трудоустройство';

export const PERIOD_TYPE: Record<string, PeriodType> = {
    registration: 'регистрация',
    inpatient: 'пребывание в стационаре',
    stop_payment: 'приостановление выплаты',
    employment: 'трудоустройство',
}
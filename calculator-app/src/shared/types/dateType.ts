export type Year = number;
export type Rubles = number;
export type DateString = string; // 'YYYY-MM-DD'

export interface YearlyData {
    [year: Year]: Rubles;
}

export interface TimeSeriesData {
    [date: DateString]: Rubles;
}

export interface DateRange {
    startDate: DateString;
    endDate: DateString;
}

export interface RegistrationPeriod extends DateRange {
    id: string;
}
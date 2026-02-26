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
    DN: DateString;
    DK: DateString;
}

export interface DatePeriod extends DateRange {
    id: number;
}
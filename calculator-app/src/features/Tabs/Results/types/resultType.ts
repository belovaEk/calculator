import { DateRange, DatePeriod, DateString, Rubles } from "../../../../shared";
import { PaymentInterface } from "../../Payments/components/types/paymentType";
import { OrderType } from "../../../../store/type";

export type RowType = {
    pmpOrGss: string;
    startDate: DateString;
    endDate: DateString;
    spAmount?: string;
    pmpGssAmount?: string
    rsdAmount?: string
};


export interface ResultsRequestData {
    is_adult: boolean;
    date_of_birth: string;
    document_on_full_time_OOP_education?: boolean;
    is_there_a_registration_in_moscow: boolean;
    is_there_a_registration_in_moscow_of_the_breadwinner: boolean | string;
    is_there_a_registration_in_moscow_of_the_legal_representative: boolean;
    periods_reg_moscow: Array<any>;
    periods_reg_representative_moscow?: Array<any>;
    periods_reg_breadwinner_moscow?: Array<any>;
    date_of_death_of_the_breadwinner?: string;
    there_is_a_breadwinner: boolean;
    payments: Array<PaymentInterface>;
    periods_suspension?: Array<DatePeriod>;
    periods_inpatient?: Array<DatePeriod> | undefined;

    periods_employment?: Array<DatePeriod>;
    is_order?: boolean;
    orders_date?: Array<OrderType>
    change_last_date?: DateString

    [key: string]: any; // Индексная сигнатура для доступа по строке
}



export interface GssPmpI {
    [id: number]: Array<DateRange>
}

export interface RsdItem {
  DN: DateString; 
  DK: DateString;     
  amount: Rubles;
  pmp_or_gss: string;  
  sp_amount: Rubles;
  pmp_gss_amount: Rubles
}

export type RsdList = RsdItem[];

export interface RadGssPmpI {
    [id: number]: RsdItem[]
}

export interface PromiseI {
    message?: string,
    pmp_periods?: GssPmpI,
    gss_periods?: GssPmpI,
    sorted_pensions?: {
        [key: string]: RsdItem[]
    },
}


export type JsonDataWithIndex = {
    [key: string]: any;
};
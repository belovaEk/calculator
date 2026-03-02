import { DateRange, DatePeriod } from "../../../../shared";
import { PaymentInterface } from "../../Payments/components/types/paymentType";


export type RowType = {
    paymentType: string;
    pensionType: string;
    startDate: string;
    endDate: string;
};


export interface ResultsRequestData {
    is_adult: boolean;
    date_of_birth: string;
    document_on_full_time_OOP_education: boolean;
    type_of_social_payment: string;
    is_there_a_registration_in_moscow: boolean;
    is_there_a_registration_in_moscow_of_the_breadwinner: boolean | string;
    is_there_a_registration_in_moscow_of_the_legal_representative: boolean;
    periods_reg_moscow: Array<any>;
    periods_reg_representative_moscow: Array<any>;
    periods_reg_breadwinner_moscow: Array<any>;
    date_of_death_of_the_breadwinner: string;
    there_is_a_breadwinner: boolean;
    is_payment_transferred: any;
    is_get_PSD_FSD_last_mounth_payment_trasferred: any;
    is_Not_get_PSD_FSD_now_payment_trasferred: any;
    payments: Array<PaymentInterface>;
    periods_suspension: Array<DatePeriod>;
    periods_inpatient: Array<DatePeriod> | undefined;
    [key: string]: any; // Индексная сигнатура для доступа по строке
}



export interface GssPmpI {
    [id: number]: Array<DateRange>
}

export interface PromiseI {
    message?: string,
    pmp_periods?: GssPmpI,
    gss_periods?: GssPmpI,
}


export type JsonDataWithIndex = {
    [key: string]: any;
};
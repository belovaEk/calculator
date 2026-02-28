import { DateString, DatePeriod } from "../shared";
import { PaymentInterface } from "../features/Tabs/Payments/components/types/paymentType";

export interface GlobalStoreContextInterface {
    store: GlobalStoreParameterInterface;
    updateStore: <K extends keyof GlobalStoreParameterInterface>(parametr: K, value: GlobalStoreParameterInterface[K]) => void;
    resetStore: () => void;
}

export interface GlobalStoreParameterInterface {
    is_adult?: boolean,
    date_of_birth?: DateString,
    // document_on_full_time_OOP_education?: boolean,
    type_of_social_payment?: string,
    is_there_a_registration_in_moscow_of_the_breadwinner?: boolean,
    is_there_a_registration_in_moscow_of_the_legal_representative?: boolean,
    is_there_a_registration_in_moscow?: boolean,
    periods_of_registration_in_moscow?: Array<DatePeriod>,
    periods_of_registration_in_moscow_of_the_breadwinner?: Array<DatePeriod>,
    periods_of_registration_in_moscow_of_the_legal_representative?: Array<DatePeriod>,
    date_of_appointment_of_the_spv?: DateString,
    date_of_death_of_the_breadwinner?: DateString,

    is_inpatient?: boolean,
    periods_of_inpatient?: Array<DatePeriod>,

    there_is_a_breadwinner?: boolean,

    is_payment_transferred?: boolean,
    is_get_PSD_FSD_last_mounth_payment_trasferred?: boolean,
    is_Not_get_PSD_FSD_now_payment_trasferred?: boolean,

    payments?: Array<PaymentInterface>,
}

    
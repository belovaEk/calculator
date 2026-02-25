import { DateRange } from "../shared";

export interface GlobalStoreContextInterface {
    store: GlobalStoreParameterInterface;
    updateStore: <K extends keyof GlobalStoreParameterInterface>(parametr: K, value: GlobalStoreParameterInterface[K]) => void;
}

export interface GlobalStoreParameterInterface {
    is_adult?: boolean,
    age?: number,
    document_on_full_time_OOP_education?: boolean,
    date_of_the_initial_appointment_of_the_SPV_is_137_or_143?: string,
    type_of_social_payment?: string,
    is_there_a_registration_in_moscow?: boolean,
    the_periods_of_registration_in_moscow_of_the_child?: Array<DateRange>,
    periods_of_registration_of_the_breadwinner_or_legal_representative_in_moscow?: Array<DateRange>,
    date_of_appointment_of_the_spv?: string,
    breadwinner_or_legal_representative?: string,
    date_of_death_of_the_breadwinner?: string,
    date_of_the_initial_appointment_of_the_spv_01_067?: string,
}


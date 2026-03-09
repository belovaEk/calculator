import { DateString, DatePeriod } from "../shared";
import { PaymentInterface } from "../features/Tabs/Payments/components/types/paymentType";


export interface GlobalStoreContextInterface {
    store: GlobalStoreParameterInterface;
    updateStore: <K extends keyof GlobalStoreParameterInterface>(parametr: K, value: GlobalStoreParameterInterface[K]) => void;
    resetStore: () => void;
}

export interface OrderType {
    id: number,
    date: DateString
}

export interface GlobalStoreParameterInterface {
    is_adult: boolean,
    date_of_birth: DateString,
    // document_on_full_time_OOP_education?: boolean,
    // type_of_social_payment?: string,

    // Наличие периодов регистрации
    is_there_a_registration_in_moscow: boolean,
    is_there_a_registration_in_moscow_of_the_breadwinner: boolean,
    is_there_a_registration_in_moscow_of_the_legal_representative: boolean,

    // Периоды регистрации
    periods_reg_moscow?: Array<DatePeriod>,
    periods_reg_breadwinner_moscow?: Array<DatePeriod>,
    periods_reg_representative_moscow?: Array<DatePeriod>,

    // Кормилец
    is_breadwinner: boolean,
    date_of_death_of_the_breadwinner?: DateString,


    // Стационаризация
    is_inpatient: boolean,
    periods_inpatient?: Array<DatePeriod>,

    // трудоустройство
    is_employment: boolean,
    periods_employment?: Array<DatePeriod>,
    
    // Выплаты
    payments: Array<PaymentInterface>,
    
    // приостановки
    is_suspension: boolean,
    periods_suspension?: Array<DatePeriod>,

    // дата последнего изменения вида пенсии
    change_last_date?: DateString,

    // заявления на ГСС
    is_order: boolean,
    orders_date?: Array<OrderType>

}



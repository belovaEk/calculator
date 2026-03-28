import { Rubles } from "../../../../../shared";
import { DateString } from "../../../../../shared";

export type PaymentTypeRaw = 'pension' | 'edv' | 'egdv' | 'housing' | 'edk';
export type PaymentTypeDisplay = 'Пенсия' | 'ЕДВ' | 'ЕГДВ' | 'ЖКУ' | 'Другая выплата';

export type PensionCategoryRaw = 'insurance_SPK' | 'social_SPK' | 'social_disability' | 'departmental';

// export type PensionCategoryAdultRaw = 'insurance' | 'social' | 'departmental' | 'gosudarstvennaya' | 'other' | 'monthPay';
export type PensionCategoryAdultRaw = 'insurance_SPK' | 'insurance_disability' | 'insurance_age' | 'social_SPK' | 'social_disability' | 'social_age' | 'departmental_SPK'
    | 'departmental_age' | 'departmental_disability' | 'gosudarstvennaya_SPK' | 'gosudarstvennaya_age' | 'gosudarstvennaya_disability' | 'accumulative' |
    'part_insurance' | 'ldnr' | 'zo' | 'ho' | 'disability' | 'spk' | 'length_of_service' | 'temporary_monthl' | 'monthl'

export type PersonCategoryRaw = 'reabilitirovan' | 'truzhennik' | 'war_child' | 'labor_veteran' | 'labor_veteran_55_60'

export interface RecalculationData {
    date: DateString,
    amount: Rubles
}

export interface PaymentInterface {
    id: number,
    type: PaymentTypeRaw,
    categoria: PensionCategoryRaw | PensionCategoryAdultRaw | '',
    DN: DateString,
    DK: DateString,
    amount: Rubles,
    is_Moscow: boolean,
    is_recalculation?: boolean,
    recalculation?: RecalculationData[]

    is_payment_transferred: boolean,
    is_get_PSD_FSD_last_mounth_payment_trasferred?: boolean,
    is_get_PSD_FSD_last_year_payment_trasferred?: boolean,
    is_Not_get_PSD_FSD_now_payment_trasferred?: boolean,

    // invalid_categoria?: '' | '1' | '2' | '3',
    // num_dependents?: number

    is_fix_amoumt: boolean
    amount_fix?: Rubles,
    is_recalculation_fix_amount?: boolean,
    recalculation_fix_amount?: RecalculationData[]
    categoria_person?: PersonCategoryRaw
}

export interface PaymentProps {
    id: number,
    index: number,
    paymentData: PaymentInterface,
    onUpdate: (id: number, updatedPayment: PaymentInterface) => void,
    onRemove: (id: number) => void,
}



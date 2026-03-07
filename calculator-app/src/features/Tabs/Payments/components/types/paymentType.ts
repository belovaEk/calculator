import { Rubles } from "../../../../../shared";
import { DateString } from "../../../../../shared";

export type PaymentTypeRaw = 'pension' | 'edv' | 'egdv' | 'housing' | 'custom';
export type PaymentTypeDisplay = 'Пенсия' | 'ЕДВ' | 'ЕГДВ' | 'ЖКУ' | 'Другая выплата';

export type PensionCategoryRaw = 'insurance_SPK' | 'social_SPK' | 'social_disability' | 'departmental';
export type PensionCategoryDisplay = 'Страховая по СПК' | 'Социальная по СПК' | 'Социальная по инвалидности' | 'Ведомственная';


export interface RecalculationData {
    date: DateString,
    amount: Rubles
}

export interface PaymentInterface {
    id: number,
    type: PaymentTypeRaw,
    categoria: PensionCategoryRaw | '',
    DN: DateString,
    DK: DateString,
    amount: Rubles,
    is_Moscow: boolean,
    is_recalculation?: boolean,
    recalculation?: RecalculationData[]

    is_payment_transferred: boolean,
    is_get_PSD_FSD_last_mounth_payment_trasferred: boolean,
    is_get_PSD_FSD_last_year_payment_trasferred: boolean,
    is_Not_get_PSD_FSD_now_payment_trasferred: boolean,
}

export interface PaymentProps  {
    id: number,
    index: number,
    paymentData: PaymentInterface,
    onUpdate: (id: number, updatedPayment: PaymentInterface) => void,
    onRemove: (id: number) => void,
}



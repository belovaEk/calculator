import { Rubles } from "../../../../../shared";
import { DateString } from "../../../../../shared";

export type PaymentTypeRaw = 'pension' | 'edv' | 'egdv' | 'housing' | 'custom';
export type PaymentTypeDisplay = 'Пенсия' | 'ЕДВ' | 'ЕГДВ' | 'ЖКУ' | 'Другая выплата';

export type PensionCategoryRaw = 'insurance_SPK' | 'social_SPK' | 'social_disability';
export type PensionCategoryDisplay = 'Страховая по СПК' | 'Социальная по СПК' | 'Социальная по инвалидности';

export interface PaymentInterface {
    id: number,
    type: PaymentTypeRaw,
    categoria: PensionCategoryRaw | '',
    DN: DateString,
    DK: DateString,
    paymentAmount: Rubles,
    is_Moscow: boolean
}

export interface PaymentProps  {
    id: number,
    index: number,
    paymentData: PaymentInterface,
    onUpdate: (id: number, updatedPayment: PaymentInterface) => void,
    onRemove: (id: number) => void,
}



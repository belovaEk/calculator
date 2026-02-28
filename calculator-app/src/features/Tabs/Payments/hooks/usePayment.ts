import { PAYMENT_TYPE, PENSION_CATEGORIES } from "../constants/payment";
import { PaymentInterface } from "../components/types/paymentType";


interface usePaymentParams {
    id: number,
    paymentData: PaymentInterface,
    onUpdate: (id: number, updatedPayment: PaymentInterface) => void,
    onRemove: (id: number) => void,
}


export const usePayment = ({ id, paymentData, onUpdate, onRemove }: usePaymentParams) => {

    const updatePayment = (field: keyof PaymentInterface, value: any) => {
        const updated = {
            ...paymentData,
            [field]: value
        };
        onUpdate(id, updated);
    };


    const handleRemove = () => {
        onRemove(id);
    };

    const handleCurrentDate = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.checked) {
            updatePayment('DK', new Date().toISOString().split('T')[0]);
        } else {
            updatePayment('DK', '');
        }
    };


    return {
        PAYMENT_TYPE,
        PENSION_CATEGORIES,
        updatePayment,
        handleRemove,
        handleCurrentDate,
    }
}


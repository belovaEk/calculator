import { PAYMENT_TYPE, PENSION_CATEGORIES } from "../constants/payment";
import { PaymentInterface, RecalculationData } from "../components/types/paymentType";


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


    const addRecalculation = () => {
        const newRecalculation: RecalculationData = {
            date: '',
            amount: 0
        };

        const currentRecalculations = paymentData.recalculation || [];
        const updatedRecalculations = [...currentRecalculations, newRecalculation];

        updatePayment('recalculation', updatedRecalculations);
    };

    const updateRecalculation = (
        paymentId: number,
        recalIndex: number,
        field: keyof RecalculationData,
        value: any
    ) => {
        // Проверяем, что это тот же payment
        if (paymentId !== id) return;

        const currentRecalculations = paymentData.recalculation || [];
        const updatedRecalculations = [...currentRecalculations];

        if (!updatedRecalculations[recalIndex]) {
            updatedRecalculations[recalIndex] = { date: '', amount: 0 };
        }

        updatedRecalculations[recalIndex] = {
            ...updatedRecalculations[recalIndex],
            [field]: value
        };

        updatePayment('recalculation', updatedRecalculations);
    };

    // Удаление перерасчета
    const removeRecalculation = (paymentId: number, recalIndex: number) => {
        if (paymentId !== id) return;

        const currentRecalculations = paymentData.recalculation || [];
        const updatedRecalculations = currentRecalculations.filter((_, index) => index !== recalIndex);

        updatePayment('recalculation', updatedRecalculations);

        // Если перерасчетов больше нет, можно сбросить флаг
        if (updatedRecalculations.length === 0) {
            updatePayment('is_recalculation', false);
        }
    };


    return {
        PAYMENT_TYPE,
        PENSION_CATEGORIES,
        updatePayment,
        handleRemove,
        handleCurrentDate,
        addRecalculation,
        updateRecalculation,
        removeRecalculation,
    }
}


import { PENSION_CATEGORIES_CHILDREN } from "../constants/children/paymentCategories";
import { PENSION_CATEGORIES_ADULT } from "../constants/adult/paymentCategories";
import { PaymentInterface, RecalculationData } from "../components/types/paymentType";
import { PAYMENT_TYPE } from "../constants/payments"
import { useGlobalStore } from "../../../../store";
import { PERSON_CATEGORIES } from "../constants/adult/peopleCategories";
import { useState } from "react";

interface usePaymentParams {
    id: number,
    paymentData: PaymentInterface,
    onUpdate: (id: number, updatedPayment: PaymentInterface) => void,
    onRemove: (id: number) => void,
}


export const usePayment = ({ id, paymentData, onUpdate, onRemove }: usePaymentParams) => {


    const { store } = useGlobalStore();

    const updatePayment = (field: keyof PaymentInterface, value: any) => {
        // Если изменяется поле categoria
        if (field === 'categoria') {
            // Сохраняем поля, которые не должны сбрасываться
            const preservedFields = {
                id: paymentData.id,
                type: paymentData.type,
                DN: paymentData.DN,
                DK: paymentData.DK,
                is_Moscow: paymentData.is_Moscow,
            };

            // Создаем новый объект с сохраненными полями и новой категорией
            const updated = {
                ...preservedFields,
                categoria: value,

                // Сбрасываем все остальные поля в значения по умолчанию
                amount: 0,
                is_payment_transferred: false,
                is_fix_amoumt: false,
            };

            onUpdate(id, updated);
        } else {
            // Для всех остальных полей - обычное обновление
            const updated = {
                ...paymentData,
                [field]: value
            };
            onUpdate(id, updated);
        }
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
        // Проверяем, что это тот же payment (paymentId теперь равен индексу)
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

        // Если перерасчетов больше нет, можно сбросить флаг
        if (updatedRecalculations.length === 0) {
            // Если массив пустой, удаляем его полностью
            const updatedPayment = {
                ...paymentData,
                recalculation: undefined, // Устанавливаем в undefined вместо пустого массива
                is_recalculation: false
            };
            onUpdate(id, updatedPayment);
        } else {
            // Если есть элементы, обновляем массив
            updatePayment('recalculation', updatedRecalculations);
        }
    };


    const addRecalculationFixAmount = () => {
        const newRecalculation: RecalculationData = {
            date: '',
            amount: 0
        };

        const currentRecalculations = paymentData.recalculation_fix_amount || [];
        const updatedRecalculations = [...currentRecalculations, newRecalculation];

        updatePayment('recalculation_fix_amount', updatedRecalculations);
    };

    const updateRecalculationFixAmount = (
        paymentId: number,
        recalIndex: number,
        field: keyof RecalculationData,
        value: any
    ) => {
        if (paymentId !== id) return;

        const currentRecalculations = paymentData.recalculation_fix_amount || [];
        const updatedRecalculations = [...currentRecalculations];

        if (!updatedRecalculations[recalIndex]) {
            updatedRecalculations[recalIndex] = { date: '', amount: 0 };
        }

        updatedRecalculations[recalIndex] = {
            ...updatedRecalculations[recalIndex],
            [field]: value
        };

        updatePayment('recalculation_fix_amount', updatedRecalculations);
    };

    const removeRecalculationFixAmount = (paymentId: number, recalIndex: number) => {
        if (paymentId !== id) return;

        const currentRecalculations = paymentData.recalculation_fix_amount || [];
        const updatedRecalculations = currentRecalculations.filter((_, index) => index !== recalIndex);

        if (updatedRecalculations.length === 0) {
            // Если массив пустой, удаляем его полностью
            const updatedPayment = {
                ...paymentData,
                recalculation_fix_amount: undefined, // Устанавливаем в undefined вместо пустого массива
                is_recalculation_fix_amount: false
            };
            onUpdate(id, updatedPayment);
        } else {
            // Если есть элементы, обновляем массив
            updatePayment('recalculation_fix_amount', updatedRecalculations);
        }
    };


    const today = new Date().toISOString().split('T')[0];

    const checkDate = (date: string) => {
        if (date > today) {
            updatePayment('DK', today);
            return false;
        }
        updatePayment('DK', date);
        return true;
    };


    return {
        store,
        PAYMENT_TYPE,
        PENSION_CATEGORIES_CHILDREN,
        PENSION_CATEGORIES_ADULT,
        updatePayment,
        handleRemove,
        handleCurrentDate,
        addRecalculation,
        updateRecalculation,
        removeRecalculation,
        addRecalculationFixAmount,
        updateRecalculationFixAmount,
        removeRecalculationFixAmount,
        PERSON_CATEGORIES,
        checkDate
    }
}


import { useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";
import { PaymentInterface } from "../components/types/paymentType";
import { PaymentTypeRaw } from "../components/types/paymentType";
import { useGlobalStore } from "../../../../store";
import {PAYMENT_TYPE} from "../constants/payments"

export const usePayments = () => {
    const navigate = useNavigate();

    const { store, updateStore } = useGlobalStore();

    const getPaymentsFromStore = (): PaymentInterface[] => {
        const storedPayments = store.payments || [];
        return storedPayments.map((payment, index) => ({
            ...payment,
            id: index
        }));
    };

    const [payments, setPayments] = useState<Array<PaymentInterface>>(() => {
        const storedPayments = getPaymentsFromStore();
        return storedPayments;
    });


    const addPaymet = (type: PaymentTypeRaw) => {
        const newPayment: PaymentInterface = {
            id: payments.length,
            type: type,
            categoria: '',
            DN: '',
            DK: '',
            amount: 0,
            is_Moscow: false,
            is_payment_transferred: false,
            is_fix_amoumt: false,

        };

        setPayments(prev => [...prev, newPayment]);
        return payments.length
    }


    const updatePayment = (id: number, updatedPayment: PaymentInterface) => {
         setPayments(prev =>
            prev.map((payment, index) => {
                if (index === id) {
                    return {
                        ...updatedPayment,
                        id: index 
                    };
                }
                return payment;
            })
        );
    };

    const updateGlobalPayments = () => {
        updateStore('payments', payments);
    };

    useEffect(() => {
        updateGlobalPayments()
    }, [payments])


    const removePayment = (id: number) => {
        setPayments(prev => {
            // Фильтруем и перенумеровываем
            const filtered = prev.filter((_, index) => index !== id);
            return filtered.map((payment, index) => ({
                ...payment,
                id: index
            }));
        });
    };

    return {
        store,
        updateStore,
        navigate,
        payments,
        addPaymet,
        updatePayment,
        removePayment,
        PAYMENT_TYPE
    }
}
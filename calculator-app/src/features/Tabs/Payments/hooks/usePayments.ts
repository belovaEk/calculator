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
        return store.payments || [];
    };

    const [payments, setPayments] = useState<Array<PaymentInterface>>(() => {
        const storedPayments = getPaymentsFromStore();
        return storedPayments;
    });

    const [nextId, setNextId] = useState<number>(() => {
        const storedPayments = getPaymentsFromStore();
        return storedPayments.length > 0
            ? Math.max(...storedPayments.map(p => p.id)) + 1
            : 0;
    });


    const addPaymet = (type: PaymentTypeRaw) => {
        const newPayment: PaymentInterface = {
            id: nextId,
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
        setNextId(id => id + 1);
        return nextId;
    }


    const updatePayment = (id: number, updatedPayment: PaymentInterface) => {
        setPayments(prev =>
            prev.map(payment =>
                payment.id === id ? updatedPayment : payment
            )
        );
    };

    const updateGlobalPayments = () => {
        updateStore('payments', payments);
    };

    useEffect(() => {
        updateGlobalPayments()
    }, [payments])


    const removePayment = (id: number) => {
        setPayments(prev => prev.filter(payments => payments.id !== id))
    }

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
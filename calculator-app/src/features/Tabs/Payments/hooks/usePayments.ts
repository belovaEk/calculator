import { useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";
import { PaymentInterface } from "../components/types/paymentType";
import { PaymentTypeRaw } from "../components/types/paymentType";
import { useGlobalStore } from "../../../../store";
import { PAYMENT_TYPE } from "../constants/payment";

export const usePayments = () => {
    const navigate = useNavigate();

    const { updateStore } = useGlobalStore();

    const [payments, setPayments] = useState<Array<PaymentInterface>>([]);
    const [nextId, setNextId] = useState<number>(0);


    const addPaymet = (type: PaymentTypeRaw) => {
        const newPayment: PaymentInterface = {
            id: nextId,
            type: type,
            categoria: '',
            DN: '',
            DK: '',
            paymentAmount: 0,
            is_Moscow: false,
            is_suspension: false,
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
    }, payments)


    const removePayment = (id: number) => {
        setPayments(prev => prev.filter(payments => payments.id !== id))
    }

    return {
        navigate,
        payments,
        addPaymet,
        updatePayment,
        removePayment,
        PAYMENT_TYPE
    }
}
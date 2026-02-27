import { useEffect, useState } from "react";
import { DatePeriod } from "../../..";
import { useGlobalStore } from "../../../../store";
import { PERSONA, personaType } from "../../../constants/people";
import { PeriodType, PERIOD_TYPE } from "../../../constants/periodsName";

export const usePeriods = (persona: personaType, typePeriod: PeriodType, paymentId?: number) => {

    const { store, updateStore } = useGlobalStore();

    const currentPayments = store.payments || [];

    const [periods, setPeriods] = useState<Array<DatePeriod>>([]);
    const [nextId, setNextId] = useState<number>(0);

    const addPeriod = () => {
        const newPeriod: DatePeriod = {
            id: nextId,
            DN: '',
            DK: ''
        };
        setPeriods(prev => [...prev, newPeriod]);
        setNextId(prev => prev + 1);
        return nextId;
    };

    const updatePeriod = (id: number, updatedPeriod: DatePeriod) => {
        setPeriods(prev =>
            prev.map(period =>
                period.id === id ? updatedPeriod : period
            )
        );
    };

    const updatePeriodRegistration = () => {
        if (persona === PERSONA.children || persona === PERSONA.adult) {
            updateStore('periods_of_registration_in_moscow', periods);
            return;
        }
        if (persona === PERSONA.legal_representative) {
            updateStore('periods_of_registration_in_moscow_of_the_legal_representative', periods);
            return;
        }
        if (persona === PERSONA.breadwinner) {
            updateStore('periods_of_registration_in_moscow_of_the_breadwinner', periods);
            return;
        }
    }

    const updatePeriodInpatient = () => {
        updateStore('periods_of_inpatient', periods);
    }

    const updatedPayments = currentPayments.map(payment => {
        if (payment.id === paymentId) {
            return {
                ...payment,
                suspension: periods,
                is_suspension: periods.length > 0
            };
        }
        return payment;
    });

    const updateGlobalPeriodStopPayment = () => {
        updateStore('payments', updatedPayments)
    }

    useEffect(() => {
        if (typePeriod === PERIOD_TYPE.registration) {
            updatePeriodRegistration();
            return;
        }
        if (typePeriod === PERIOD_TYPE.inpatient) {
            updatePeriodInpatient();
            return;
        }
        if (typePeriod === PERIOD_TYPE.stop_payment) {
            updateGlobalPeriodStopPayment();
            return;
        }

    }, periods);

    const removePeriod = (id: number) => {
        setPeriods(prev => prev.filter(periods => periods.id !== id));
    };

    return {
        store,
        periods,
        addPeriod,
        updatePeriod,
        removePeriod
    };
};
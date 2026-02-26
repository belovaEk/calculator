import { useEffect, useState } from "react";
import { DatePeriod } from "../../..";
import { useGlobalStore } from "../../../../store";
import { PERSONA, personaType } from "../../../constants/people";
import { periodType, PERIOD_TYPE } from "../../../constants/periodsName";

export const usePeriods = (persona: personaType, typePeriod: periodType) => {

    const { store, updateStore } = useGlobalStore();

    const [periods, setPeriods] = useState<Array<DatePeriod>>([]);
    const [nextId, setNextId] = useState<number>(1);

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
        if (persona === PERSONA.representative) {
            updateStore('periods_of_registration_in_moscow_of_the_breadwinner_or_legal_representative', periods);
            return;
        }
    }

    const updatePeriodInpatient = () => {
        updateStore('periods_of_inpatient', periods);
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

    }, periods);

    const removePeriod = (id: number) => {
        setPeriods(prev => prev.filter(period => period.id !== id));
    };

    return {
        store,
        periods,
        addPeriod,
        updatePeriod,
        removePeriod
    };
};
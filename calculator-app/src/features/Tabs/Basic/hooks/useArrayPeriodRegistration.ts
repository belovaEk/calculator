import { useEffect, useState } from "react";
import { RegistrationPeriod } from "../../../../shared";
import { useGlobalStore } from "../../../../store";

export const useArrayPeriodRegistration = (persona: string) => {

    const {updateStore} = useGlobalStore();

    const [periods, setPeriods] = useState<Array<RegistrationPeriod>>([]);
    const [nextId, setNextId] = useState<number>(1);

    const addPeriod = () => {
        const newPeriod: RegistrationPeriod = {
            id: nextId,
            DNreg: '',
            DKreg: ''
        };
        setPeriods(prev => [...prev, newPeriod]);
        setNextId(prev => prev + 1);
        return nextId;
    };

    const updatePeriod = (id: number, updatedPeriod: RegistrationPeriod) => {
        setPeriods(prev =>
            prev.map(period =>
                period.id === id ? updatedPeriod : period
            )
        );
    };

    useEffect(()=> {
        if (persona === 'ребенка') {
            updateStore('periods_of_registration_in_moscow_of_the_child', periods);
        } 
        if (persona === 'законного представителя или кормильца') {
            updateStore('periods_of_registration_in_moscow_of_the_breadwinner_or_legal_representative', periods)
        }
    }, periods);

    const removePeriod = (id: number) => {
        setPeriods(prev => prev.filter(period => period.id !== id));
    };

    return {
        periods,
        addPeriod,
        updatePeriod,
        removePeriod
    };
};
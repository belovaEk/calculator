import { useEffect, useState } from "react";
import { DatePeriod } from "../../..";
import { useGlobalStore } from "../../../../store";
import { PERSONA, personaType } from "../../../constants";
import { PeriodType, PERIOD_TYPE } from "../../../constants";

export const usePeriods = (persona: personaType, typePeriod: PeriodType) => {

    const { store, updateStore } = useGlobalStore();


    const getPeriodsFromStore = (): DatePeriod[] => {
        if (typePeriod === PERIOD_TYPE.registration) {
            if (persona === PERSONA.children || persona === PERSONA.adult) {
                return store.periods_reg_moscow || [];
            }
            if (persona === PERSONA.legal_representative) {
                return store.periods_reg_representative_moscow || [];
            }
            if (persona === PERSONA.breadwinner) {
                return store.periods_reg_breadwinner_moscow || [];
            }
        }
        if (typePeriod === PERIOD_TYPE.inpatient) {
            return store.periods_inpatient || [];
        }
        if (typePeriod === PERIOD_TYPE.stop_payment) {
            return store.periods_suspension || [];
        }
        if (typePeriod === PERIOD_TYPE.employment) {
            return store.periods_employment || [];
        }
        return [];
    };
    
    const [periods, setPeriods] = useState<DatePeriod[]>(() => {
        const storedPeriods = getPeriodsFromStore();
        return storedPeriods;
    });
    

    const [nextId, setNextId] = useState<number>(() => {
        const storedPeriods = getPeriodsFromStore();
        return storedPeriods.length > 0 
            ? Math.max(...storedPeriods.map(p => p.id)) + 1 
            : 0;
    });

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
            updateStore('periods_reg_moscow', periods);
            return;
        }
        if (persona === PERSONA.legal_representative) {
            updateStore('periods_reg_representative_moscow', periods);
            return;
        }
        if (persona === PERSONA.breadwinner) {
            updateStore('periods_reg_breadwinner_moscow', periods);
            return;
        }
    }

    const updatePeriodInpatient = () => {
        updateStore('periods_inpatient', periods);
    }

    const updateGlobalPeriodSuspension = () => {
        updateStore('periods_suspension', periods)
    }

     const updateGlobalPeriodEmployment = () => {
        updateStore('periods_employment', periods)
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
            updateGlobalPeriodSuspension();
            return;
        }
        if (typePeriod === PERIOD_TYPE.employment) {
            updateGlobalPeriodEmployment();
            return;
        }

    }, [periods]);

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
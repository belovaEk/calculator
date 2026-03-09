import { useEffect, useState } from "react";
import { DatePeriod } from "../../..";
import { useGlobalStore } from "../../../../store";
import { PERSONA, personaType } from "../../../constants";
import { PeriodType, PERIOD_TYPE } from "../../../constants";

export const usePeriods = (persona: personaType, typePeriod: PeriodType) => {

    const { store, updateStore } = useGlobalStore();


    const getPeriodsFromStore = (): DatePeriod[] => {

        let storedPeriods: DatePeriod[] = [];

        if (typePeriod === PERIOD_TYPE.registration) {
            if (persona === PERSONA.children || persona === PERSONA.adult) {
                storedPeriods = store.periods_reg_moscow || [];
            }
            if (persona === PERSONA.legal_representative) {
                storedPeriods = store.periods_reg_representative_moscow || [];
            }
            if (persona === PERSONA.breadwinner) {
                storedPeriods = store.periods_reg_breadwinner_moscow || [];
            }
        }
        if (typePeriod === PERIOD_TYPE.inpatient) {
            storedPeriods = store.periods_inpatient || [];
        }
        if (typePeriod === PERIOD_TYPE.stop_payment) {
            storedPeriods = store.periods_suspension || [];
        }
        if (typePeriod === PERIOD_TYPE.employment) {
            storedPeriods = store.periods_employment || [];
        }

        return storedPeriods.map((period, index) => ({
            ...period,
            id: index
        }));
    };

    const [periods, setPeriods] = useState<DatePeriod[]>(() => {
        const storedPeriods = getPeriodsFromStore();
        return storedPeriods;
    });


    const addPeriod = () => {
        const newPeriod: DatePeriod = {
            id: periods.length,
            DN: '',
            DK: ''
        };
        setPeriods(prev => [...prev, newPeriod]);
        return periods.length;
    };

    const updatePeriod = (id: number, updatedPeriod: DatePeriod) => {
        setPeriods(prev =>
            prev.map((period, index) => {
                // Обновляем по индексу, который равен id
                if (index === id) {
                    return {
                        ...updatedPeriod,
                        id: index // Убеждаемся, что ID соответствует индексу
                    };
                }
                return period;
            })
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
        setPeriods(prev => {
            // Фильтруем по индексу
            const filtered = prev.filter((_, index) => index !== id);
            // Перенумеровываем ID в соответствии с новыми индексами
            return filtered.map((period, index) => ({
                ...period,
                id: index
            }));
        });
    };

    return {
        store,
        periods,
        addPeriod,
        updatePeriod,
        removePeriod
    };
};
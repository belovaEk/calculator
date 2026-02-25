
import { useState, useEffect,  } from "react";
import { useGlobalStore } from "../../../../store";
import { DateRange, DateString } from "../../../../shared";

export const usePeriodRegistration = () => {

    const [periodRegistration, setPeriodRegistration] = useState<DateRange>();

    const updatePeriodRegistration = <K extends keyof DateRange>(dateType: K, date: DateString) => {

        setPeriodRegistration(prev => {
            if (!prev) {
                return {
                    DNreg: dateType === 'DNreg' ? date : '',
                    DKreg: dateType === 'DKreg' ? date : ''
                } as DateRange;
            }

            return {
                ...prev,
                [dateType]: date
            };
        })    
    }


    return {
        updatePeriodRegistration,
        periodRegistration
    }

}
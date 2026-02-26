
import { useState, useEffect, } from "react";
import { useGlobalStore } from "../../../../store";
import { DateRange, DateString } from "../../..";

export const usePeriodFrom = () => {

    const [periodRegistration, setPeriodRegistration] = useState<DateRange>();

    const updatePeriod = <K extends keyof DateRange>(dateType: K, date: DateString) => {

        setPeriodRegistration(prev => {
            if (!prev) {
                return {
                    DN: dateType === 'DN' ? date : '',
                    DK: dateType === 'DK' ? date : ''
                } as DateRange;
            }

            return {
                ...prev,
                [dateType]: date
            };
        })
    }


    return {
        updatePeriod,
        periodRegistration
    }

}
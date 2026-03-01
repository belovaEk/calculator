import { useNavigate } from "react-router-dom";
import { ROUTES } from "../../../../shared/constants";
import { PERSONA } from "../../../../shared/constants/people";
import { PERIOD_TYPE } from "../../../../shared/constants/periodsName";
import { useState } from "react";


export const useInpatient = ()=> {
    const navigate = useNavigate();

    const [isInpatient, setIsInpatient] = useState(false)

    const updateIsInpatient = (value: boolean) => {
        setIsInpatient(value)
    }

    return {
        navigate,
        isInpatient,
        updateIsInpatient,
        ROUTES,
        PERSONA,
        PERIOD_TYPE,
    }
}
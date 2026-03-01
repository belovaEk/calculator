import { useNavigate } from "react-router-dom";
import { useGlobalStore } from "../../../../store";
import { ROUTES } from "../../../../shared/constants";
import { PERSONA } from "../../../../shared/constants/people";
import { PERIOD_TYPE } from "../../../../shared/constants/periodsName";
import { useState } from "react";


export const useSuspension = ()=> {
    const navigate = useNavigate();
    const { store, updateStore } = useGlobalStore();

    const [isSuspension, setIsSuspension] = useState(false);

    const updateIsSuspension = (value: boolean) => {
        setIsSuspension(value);
    }

    return {
        navigate,
        store,
        updateStore,
        isSuspension,
        updateIsSuspension,
        ROUTES,
        PERSONA,
        PERIOD_TYPE,
    }
}
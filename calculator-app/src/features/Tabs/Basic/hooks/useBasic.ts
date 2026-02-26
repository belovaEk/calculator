import { useNavigate } from "react-router-dom";
import { useGlobalStore } from "../../../../store";
import { ROUTES } from "../../../../shared/constants";
import { PERSONA } from "../../../../shared/constants/people";
import { PERIOD_TYPE } from "../../../../shared/constants/periodsName";
import { useState } from "react";


export const useBasic = ()=> {
    const navigate = useNavigate();
    const { store, updateStore } = useGlobalStore();

    const [isVisibleSection, setIsVisibleSection] = useState(false);

    const updateIsVisibleSection = () => {
        setIsVisibleSection(prev => !prev)
    }

    return {
        navigate,
        store,
        updateStore,
        ROUTES,
        PERSONA,
        PERIOD_TYPE,
        isVisibleSection,
        updateIsVisibleSection

    }
}
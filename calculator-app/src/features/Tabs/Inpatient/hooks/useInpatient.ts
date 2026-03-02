import { useNavigate } from "react-router-dom";
import { ROUTES } from "../../../../shared/constants";
import { PERSONA } from "../../../../shared/constants/people";
import { PERIOD_TYPE } from "../../../../shared/constants/periodsName";
import { useState } from "react";
import { useGlobalStore } from "../../../../store";


export const useInpatient = ()=> {
    const navigate = useNavigate();


    const {store, updateStore} = useGlobalStore();


    return {
        navigate,
        ROUTES,
        PERSONA,
        PERIOD_TYPE,
        store,
        updateStore
    }
}
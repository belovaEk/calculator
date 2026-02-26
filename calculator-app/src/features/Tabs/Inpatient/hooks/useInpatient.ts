import { useNavigate } from "react-router-dom";
import { useGlobalStore } from "../../../../store";
import { ROUTES } from "../../../../shared/constants";
import { PERSONA } from "../../../../shared/constants/people";
import { PERIOD_TYPE } from "../../../../shared/constants/periodsName";


export const useInpatient = ()=> {
    const navigate = useNavigate();
    const { store, updateStore } = useGlobalStore();

    return {
        navigate,
        store,
        updateStore,
        ROUTES,
        PERSONA,
        PERIOD_TYPE,
    }
}
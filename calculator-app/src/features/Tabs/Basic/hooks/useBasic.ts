import { useNavigate } from "react-router-dom";
import { useGlobalStore } from "../../../../store";
import { ROUTES } from "../../../../shared/constants";


export const useBasic = ()=> {
    const navigate = useNavigate();
    const { store, updateStore } = useGlobalStore();

    return {
        navigate,
        store,
        updateStore,
        ROUTES,
    }
}
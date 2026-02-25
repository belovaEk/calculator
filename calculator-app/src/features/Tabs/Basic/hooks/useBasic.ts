import { useNavigate } from "react-router-dom";

export const useBasic = ()=> {
    const navigate = useNavigate();

    return {
        navigate
    }
}
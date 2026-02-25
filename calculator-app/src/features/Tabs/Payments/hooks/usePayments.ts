import { useNavigate } from "react-router-dom";

export const usePayments = ()=> {
    const navigate = useNavigate();

    return {
        navigate
    }
}
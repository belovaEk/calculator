import { useNavigate } from "react-router-dom";

export const useResults = ()=> {
    const navigate = useNavigate();

    return {
        navigate
    }
}
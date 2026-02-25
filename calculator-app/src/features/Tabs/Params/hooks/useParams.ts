import { useNavigate } from "react-router-dom";

export const useParams = ()=> {
    const navigate = useNavigate();

    return {
        navigate
    }
}
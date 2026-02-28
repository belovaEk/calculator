import { useNavigate } from "react-router-dom";
import { getResults } from "../services/getResults";
import { useGlobalStore } from "../../../../store";
import { useState } from "react";

export const useResults = () => {

    const navigate = useNavigate();

    const { store, resetStore } = useGlobalStore();

    const [resultData, setResultData] = useState();

    const calculate = async () => {
        const newData = await getResults(store);
        setResultData(newData);
    }

    const handlePrint = () => {
        window.print();
    }

    return {
        navigate,
        calculate,
        resultData,
        resetStore,
        handlePrint,
    }
}
import { useNavigate } from "react-router-dom";
import { getResults } from "../services/getResults";
import { useGlobalStore } from "../../../../store";
import { useState, useEffect, useCallback } from "react";
import { DatePeriod, DateRange } from "../../../../shared";
import { RowType, ResultsRequestData, PromiseI } from "../types/resultType";



export const useResults = () => {

    const navigate = useNavigate();
    const { store, resetStore } = useGlobalStore();
    const [resultData, setResultData] = useState<PromiseI>();
    const [message, setMessage] = useState('');
    const [tableData, setTableData] = useState<Array<RowType>>([]);
    const [isLoading, setIsLoading] = useState(false);

    const getJsonData = useCallback((): ResultsRequestData => {
        return {
            "is_adult": store.is_adult,
            "date_of_birth": store.date_of_birth,
            "document_on_full_time_OOP_education": true,
            "type_of_social_payment": "string",
            "is_there_a_registration_in_moscow": store?.is_there_a_registration_in_moscow || false,
            "is_there_a_registration_in_moscow_of_the_breadwinner": store?.date_of_death_of_the_breadwinner || false,
            "is_there_a_registration_in_moscow_of_the_legal_representative": store?.is_there_a_registration_in_moscow_of_the_legal_representative || false,
            "periods_reg_moscow": store?.periods_reg_moscow ?? [],
            "periods_reg_representative_moscow": store?.periods_reg_representative_moscow ?? [],
            "periods_reg_breadwinner_moscow": store?.periods_reg_breadwinner_moscow ?? [],
            "date_of_death_of_the_breadwinner": store?.date_of_death_of_the_breadwinner || "2024-01-15",
            "there_is_a_breadwinner": store?.date_of_death_of_the_breadwinner ? true : false,
            "is_payment_transferred": store.is_payment_transferred,
            "is_get_PSD_FSD_last_mounth_payment_trasferred": store.is_get_PSD_FSD_last_mounth_payment_trasferred,
            "is_Not_get_PSD_FSD_now_payment_trasferred": store.is_Not_get_PSD_FSD_now_payment_trasferred,
            "payments": store?.payments ?? [],
            "periods_suspension": store?.periods_suspension ?? [],
            "periods_inpatient": store?.periods_inpatient ?? []
        };
    }, [store]);

    const validateRequiredFields = useCallback((data: ResultsRequestData) => {
        const requiredFields: Array<keyof ResultsRequestData> = ['is_adult', 'date_of_birth', 'type_of_social_payment'];
        return requiredFields.every(field =>
            data[field] !== undefined && data[field] !== null && data[field] !== ''
        );
    }, []);


    const transformDataToTable = useCallback((data: PromiseI) => {
        const rows: Array<RowType> = [];

        // Обрабатываем ГСС
        if (data.gss_periods) {
            Object.entries(data.gss_periods).forEach(([id, periods]) => {
                periods.forEach((period: DateRange) => {
                    rows.push({
                        paymentType: 'ГСС',
                        pensionType: id,
                        startDate: period.DN,
                        endDate: period.DK
                    });
                });
            });
        }

        // Обрабатываем ПМП
        if (data.pmp_periods) {
            Object.entries(data.pmp_periods).forEach(([id, periods]) => {
                periods.forEach((period: DateRange) => {
                    rows.push({
                        paymentType: 'ПМП',
                        pensionType: id,
                        startDate: period.DN,
                        endDate: period.DK
                    });
                });
            });
        }

        setTableData(rows);
    }, []);

    
    const calculate = useCallback(async () => {
        const jsonData = getJsonData();
    
        setIsLoading(true);
        try {
            const newData: PromiseI = await getResults(jsonData);
            setResultData(newData);
            
            if (newData?.message) {
                setMessage(newData.message);
            } else {
                transformDataToTable(newData);
            }
        } catch (error) {
            console.error('Ошибка при получении результатов:', error);
        } finally {
            setIsLoading(false);
        }
    }, [getJsonData, validateRequiredFields, transformDataToTable]);


    const handlePrint = () => {
        window.print();
    }

    const handleReset = () => {
        resetStore();
        setTableData([]);
        setMessage('');
        setResultData(undefined);
    };

    return {
        navigate,
        calculate,
        tableData,
        message,
        resetStore: handleReset,
        handlePrint,
        isLoading
    }
}

import { useNavigate } from "react-router-dom";
import { getResults } from "../services/getResults";
import { useGlobalStore } from "../../../../store";
import { useState, useCallback } from "react";
import { DateRange, DateString } from "../../../../shared";
import { RowType, ResultsRequestData, PromiseI, RsdItem } from "../types/resultType";



export const useResults = () => {

    const navigate = useNavigate();
    const { store, resetStore } = useGlobalStore();
    const [resultData, setResultData] = useState<PromiseI>();
    const [message, setMessage] = useState('');
    const [tableDataPmpGss, setTableDataPmpGss] = useState<Array<RowType>>([]);
    const [tableDataPmpGssRsd, setTableDataPmpGssRsd] = useState<Array<RowType>>([]);
    const [isLoading, setIsLoading] = useState(false);

    const getJsonData = useCallback((): ResultsRequestData => {
        const data = {
            "is_adult": store.is_adult,
            "date_of_birth": store.date_of_birth,
            // "document_on_full_time_OOP_education": true,
            // "type_of_social_payment": "string",
            "is_there_a_registration_in_moscow": store.is_there_a_registration_in_moscow ?? false,
            "is_there_a_registration_in_moscow_of_the_breadwinner": store.is_adult ? null : store.is_there_a_registration_in_moscow_of_the_breadwinner ?? false,
            "is_there_a_registration_in_moscow_of_the_legal_representative": store.is_adult ? null : store.is_there_a_registration_in_moscow_of_the_legal_representative ?? false,
            "periods_reg_moscow": store.periods_reg_moscow ?? [],

            "periods_reg_representative_moscow": store.is_adult ? null : (store.is_there_a_registration_in_moscow_of_the_legal_representative ? store.periods_reg_representative_moscow : null) ,
            "periods_reg_breadwinner_moscow": store.is_adult ? null : (store.is_there_a_registration_in_moscow_of_the_breadwinner ? store.periods_reg_breadwinner_moscow : null),

            "date_of_death_of_the_breadwinner": store.is_adult ? null : (store.is_breadwinner ? store.date_of_death_of_the_breadwinner : null),
            "there_is_a_breadwinner": store.is_adult ? null : store.is_breadwinner,
            "payments": store.payments ?? [],
            "periods_suspension": store.periods_suspension ?? null,
            "periods_inpatient": store.periods_inpatient ?? null,
            "periods_employment": !(store.is_adult) ? null : store.periods_employment ?? null,
            "is_order": !(store.is_adult) ? null : store.is_order ?? false,
            "orders_date": !(store.is_adult) ? null : store.orders_date ?? null,
            "change_last_date": !(store.is_adult) ? null : store.change_last_date
        };

        // Удаляем все поля с undefined значениями
        return Object.fromEntries(
            Object.entries(data).filter(([_, value]) => value !== undefined)
        ) as ResultsRequestData;

    }, [store]);

    const validateRequiredFields = useCallback((data: ResultsRequestData) => {
        const requiredFields: Array<keyof ResultsRequestData> = ['is_adult', 'date_of_birth',];
        return requiredFields.every(field =>
            data[field] !== undefined && data[field] !== null && data[field] !== ''
        );
    }, []);


    const transformDataToTable = useCallback((data: PromiseI) => {
        const rowsPmpGss: Array<RowType> = [];
        const rowsPmpGssRsd: Array<RowType> = [];

        const formatDate = (dateStr: DateString): string => {
            if (!dateStr) return dateStr;
            const [year, month, day] = dateStr.split('-');
            return `${day}.${month}.${year}`;
        };

        if (data.message){
            setMessage(data.message)
        }
            
        // Обрабатываем ГСС
        if (data.gss_periods) {
            data.gss_periods.forEach((period: DateRange) => {
            rowsPmpGss.push({
                pmpOrGss: 'ГСС',
                startDate: formatDate(period.DN),
                endDate: formatDate(period.DK)
            });
        });
        }

        // Обрабатываем ПМП
        if (data.pmp_periods) {
            data.pmp_periods.forEach((period: DateRange) => {
            rowsPmpGss.push({
                pmpOrGss: 'ПМП',
                startDate: formatDate(period.DN),
                endDate: formatDate(period.DK)
            });
        });
        }

        // Обрабатываем ГСС и ПМП РСД
        if (data.sorted_pensions) {
            // Проходим по всем ID в объекте sorted_pensions
            Object.values(data.sorted_pensions).forEach((itemsArray: RsdItem[]) => {
                itemsArray.forEach((item: RsdItem) => {
                    rowsPmpGssRsd.push({
                        pmpOrGss: item.pmp_or_gss,
                        startDate: formatDate(item.DN),
                        endDate: formatDate(item.DK),
                        spAmount: item.sp_amount.toFixed(2),
                        rsdAmount: item.amount.toFixed(2),
                        pmpGssAmount: item.pmp_gss_amount.toFixed(2)

                    });
                });
            });
        }


        setTableDataPmpGss(rowsPmpGss);
        setTableDataPmpGssRsd(rowsPmpGssRsd)
    }, []);


    const calculate = useCallback(async () => {
        const jsonData = getJsonData();
        const startTime = Date.now();

        setIsLoading(true);
        try {
            const newData: PromiseI = await getResults(jsonData);

            const elapsedTime = Date.now() - startTime;
            const remainingTime = Math.max(0, 700 - elapsedTime);

            if (remainingTime > 0) {
                await new Promise(resolve => setTimeout(resolve, remainingTime));
            }

            setResultData(newData);

            if (newData?.message) {
                setMessage(newData.message);
            } else {
                transformDataToTable(newData);
            }
        } catch (error) {
            console.error('Ошибка при получении результатов:', error);
            const elapsedTime = Date.now() - startTime;
            const remainingTime = Math.max(0, 700 - elapsedTime);

            if (remainingTime > 0) {
                await new Promise(resolve => setTimeout(resolve, remainingTime));
            }
        } finally {
            setIsLoading(false);
        }
    }, [getJsonData, validateRequiredFields, transformDataToTable]);


    const handlePrint = () => {
        window.print();
    }

    const handleReset = () => {
        resetStore();
        setTableDataPmpGss([]);
        setTableDataPmpGssRsd([]);
        setMessage('');
        setResultData(undefined);
    };

    return {
        navigate,
        calculate,
        tableDataPmpGss,
        tableDataPmpGssRsd,
        message,
        resetStore: handleReset,
        handlePrint,
        isLoading
    }
}

import React, { createContext, useState, useContext, useEffect } from 'react';
import { GlobalStoreContextInterface, GlobalStoreParameterInterface } from './type';

const initStore: GlobalStoreParameterInterface = {
    is_adult: false,
    date_of_birth: '',
    is_there_a_registration_in_moscow_of_the_breadwinner: false,
    is_there_a_registration_in_moscow_of_the_legal_representative: false,
    is_there_a_registration_in_moscow: false,
    is_inpatient: false,
    is_suspension: false,
    payments: [],
    is_breadwinner: false,
    is_order: false,
    is_employment: false
}

const GlobalStoreContext = createContext<GlobalStoreContextInterface>({
    store: initStore,
    updateStore: () => { },
    resetStore: () => { }
});

export const useGlobalStore = () => useContext(GlobalStoreContext);

export const GlobalStoreProvider = ({ children }: { children: React.ReactNode }) => {
    const [store, setStore] = useState<GlobalStoreParameterInterface>(initStore);

    const updateStore = <K extends keyof GlobalStoreParameterInterface>(parameter: K, value: GlobalStoreParameterInterface[K]) => {
        setStore(prev => {
            let newStore = { ...prev, [parameter]: value };

            // Логика для is_adult
            if (parameter === 'is_adult') {
                if (value === true) {
                    // Переключение на взрослого - сбрасываем все детские поля
                    newStore = {
                        ...newStore,
                        payments: [],
                        is_there_a_registration_in_moscow_of_the_legal_representative: false,
                        periods_reg_representative_moscow: [],
                        is_breadwinner: false,
                        date_of_death_of_the_breadwinner: '',
                        is_there_a_registration_in_moscow_of_the_breadwinner: false,
                        periods_reg_breadwinner_moscow: [],
                    };
                } else {
                    // Переключение на ребенка - только очищаем выплаты
                    newStore = {
                        ...newStore,
                        change_last_date: '',
                        payments: [],
                        is_suspension: false,
                        periods_employment: [],
                    };
                }
            }

            // Логика для is_there_a_registration_in_moscow
            if (parameter === 'is_there_a_registration_in_moscow' && value === false) {
                newStore = {
                    ...newStore,
                    periods_reg_moscow: []
                };
            }

            // Логика для is_there_a_registration_in_moscow_of_the_breadwinner
            if (parameter === 'is_there_a_registration_in_moscow_of_the_breadwinner' && value === false) {
                newStore = {
                    ...newStore,
                    periods_reg_breadwinner_moscow: []
                };
            }

            // Логика для is_there_a_registration_in_moscow_of_the_legal_representative
            if (parameter === 'is_there_a_registration_in_moscow_of_the_legal_representative' && value === false) {
                newStore = {
                    ...newStore,
                    periods_reg_representative_moscow: []
                };
            }

            if (parameter === 'is_employment' && value === false) {
                newStore = {
                    ...newStore,
                    periods_employment: []
                };
            }

            if (parameter === 'is_suspension' && value === false) {
                newStore = {
                    ...newStore,
                    periods_suspension: []
                };
            }

            if (parameter === 'is_inpatient' && value === false) {
                newStore = {
                    ...newStore,
                    periods_inpatient: []
                };
            }

            if (parameter === 'is_order' && value === false) {
                newStore = {
                    ...newStore,
                    orders_date: []
                };
            }

            return newStore;
        });
        console.log(parameter, value);
    };

    const resetStore = () => {
        setStore(initStore);
    };

    // Логируем изменения store
    useEffect(() => {
        console.log('Store updated:', store);
    }, [store]);

    return (
        <GlobalStoreContext.Provider value={{ store, updateStore, resetStore }}>
            {children}
        </GlobalStoreContext.Provider>
    );
}; 
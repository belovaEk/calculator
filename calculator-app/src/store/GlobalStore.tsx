import React, { createContext, useState, useContext, useEffect } from 'react';
import { GlobalStoreContextInterface, GlobalStoreParameterInterface } from './type';

const initStore: GlobalStoreParameterInterface = {
    is_adult: false,
    date_of_birth: '',
    is_there_a_registration_in_moscow_of_the_breadwinner: false,
    is_there_a_registration_in_moscow_of_the_legal_representative: false,
    is_there_a_registration_in_moscow: false,
    is_payment_transferred: false,
    is_get_PSD_FSD_last_mounth_payment_trasferred: false,
    is_Not_get_PSD_FSD_now_payment_trasferred: false,
    is_inpatient: false,
    is_suspension: false,
    payments: []
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
        setStore(prev => ({ ...prev, [parameter]: value }));
        console.log(parameter, value)
    };

    const resetStore = () => {
        setStore(initStore)
    }

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
import React, { createContext, useState, useContext } from 'react';
import { GlobalStoreContextInterface, GlobalStoreParameterInterface } from './type';

const GlobalStoreContext = createContext<GlobalStoreContextInterface>({
    store: {},
    updateStore: () => { },
    resetStore: () => { }
});

export const useGlobalStore = () => useContext(GlobalStoreContext);

const initStore: GlobalStoreParameterInterface = {
    is_adult: false,
    is_there_a_registration_in_moscow_of_the_breadwinner: false,
    is_there_a_registration_in_moscow_of_the_legal_representative: false,
    there_is_a_breadwinner: false,
    is_there_a_registration_in_moscow: false,
    is_inpatient: false,
    is_payment_transferred: false,
    is_get_PSD_FSD_last_mounth_payment_trasferred: false,
    is_Not_get_PSD_FSD_now_payment_trasferred: false,
}

export const GlobalStoreProvider = ({ children }: { children: React.ReactNode }) => {

    const [store, setStore] = useState<GlobalStoreParameterInterface>(initStore);

    const updateStore = <K extends keyof GlobalStoreParameterInterface>(parameter: K, value: GlobalStoreParameterInterface[K]) => {
        setStore(prev => ({ ...prev, [parameter]: value }));
        console.log(parameter, value)
    };

    const resetStore = () => {
        setStore(initStore)
    }

    return (
        <GlobalStoreContext.Provider value={{ store, updateStore, resetStore }}>
            {children}
        </GlobalStoreContext.Provider>
    );
};
import React, { createContext, useState, useContext } from 'react';
import { GlobalStoreContextInterface, GlobalStoreParameterInterface } from './type';

const GlobalStoreContext = createContext<GlobalStoreContextInterface>({
    store: {},
    updateStore: () => { }
});

export const useGlobalStore = () => useContext(GlobalStoreContext);

const initStore: GlobalStoreParameterInterface = {
    is_adult: false,
    is_there_a_registration_in_moscow_of_the_breadwinner_or_legal_representative: false,
    is_there_a_registration_in_moscow_of_the_child: false,
    is_there_a_registration_in_moscow: false,
    is_legal_representative: true,
    is_inpatient: false,
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
        <GlobalStoreContext.Provider value={{ store, updateStore }}>
            {children}
        </GlobalStoreContext.Provider>
    );
};
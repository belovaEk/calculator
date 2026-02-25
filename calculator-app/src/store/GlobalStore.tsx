import React, { createContext, useState, useContext } from 'react';
import { GlobalStoreContextInterface, GlobalStoreParameterInterface } from './type';

const GlobalStoreContext = createContext<GlobalStoreContextInterface>({
    store: {},
    updateStore: () => { }
});

export const useGlobalStore = () => useContext(GlobalStoreContext);

export const GlobalStoreProvider = ({ children }: { children: React.ReactNode }) => {
    const [store, setStore] = useState<GlobalStoreParameterInterface>({});

    const updateStore = <K extends keyof GlobalStoreParameterInterface>(parameter: K, value: GlobalStoreParameterInterface[K]) => {
        setStore(prev => ({ ...prev, [parameter]: value }));
    };

    const resetStore = () => {
        setStore({})
    }

    return (
        <GlobalStoreContext.Provider value={{ store, updateStore }}>
            {children}
        </GlobalStoreContext.Provider>
    );
};
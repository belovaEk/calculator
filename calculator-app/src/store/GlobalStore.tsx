import React, { createContext, useState, useContext } from 'react';

interface GlobalStoreContextType {
    store: Record<string, any>;
    updateStore: (parameter: string, value: any) => void;
}

const GlobalStoreContext = createContext<GlobalStoreContextType>({
    store: {},
    updateStore: () => { }
});

export const useGlobalStore = () => useContext(GlobalStoreContext);

export const GlobalStoreProvider = ({ children }: { children: React.ReactNode }) => {
    const [store, setStore] = useState({});

    const updateStore = (parameter: string, value: any) => {
        setStore(prev => ({ ...prev, [parameter]: value }));
    };

    return (
        <GlobalStoreContext.Provider value={{ store, updateStore }}>
            {children}
        </GlobalStoreContext.Provider>
    );
};
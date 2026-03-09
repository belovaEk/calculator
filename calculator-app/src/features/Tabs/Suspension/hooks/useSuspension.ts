import { useNavigate } from "react-router-dom";
import { useGlobalStore } from "../../../../store";
import { ROUTES } from "../../../../shared/constants";
import { PERSONA } from "../../../../shared/constants/people";
import { PERIOD_TYPE } from "../../../../shared/constants/periodsName";
import { useState, useEffect } from "react"
import { OrderType } from "../../../../store/type";
import { DateString } from "../../../../shared";


export const useSuspension = () => {

    const navigate = useNavigate();
    const { store, updateStore } = useGlobalStore();

    const getOrdersDateFromStore = (): OrderType[] => {
        return store.orders_date || [];
    };

    const [ordersDate, setOrdersDates] = useState<Array<OrderType>>(() => {
        const storedOrders = getOrdersDateFromStore();
        return storedOrders;
    });

    const [nextId, setNextId] = useState<number>(() => {
        const storedOrders = getOrdersDateFromStore();
        return storedOrders.length > 0
            ? Math.max(...storedOrders.map(o => o.id)) + 1
            : 0;
    });

    const addOrder = () => {
        const newOrederDate: OrderType = {
            id: nextId,
            date: ''

        };

        setOrdersDates(prev => [...prev, newOrederDate]);
        setNextId(id => id + 1);
        return nextId;
    }

    const updateOrder = (id: number, date: DateString) => {
        setOrdersDates(prev =>
            prev.map(order =>
                order.id === id ? { ...order, date: date } : order
            )
        );
    };

    const updateGlobalPayments = () => {
        updateStore('orders_date', ordersDate);
    };

    useEffect(() => {
        updateGlobalPayments()
    }, [ordersDate])


    const removeOrder = (id: number) => {
        setOrdersDates(prev => prev.filter(ordersDate => ordersDate.id !== id))
    }

    return {
        navigate,
        store,
        updateStore,
        ROUTES,
        PERSONA,
        PERIOD_TYPE,
        ordersDate,

        addOrder,
        updateOrder,
        removeOrder
    }
}
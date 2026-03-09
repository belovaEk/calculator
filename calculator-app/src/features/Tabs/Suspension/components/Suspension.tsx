import { useSuspension } from "../hooks/useSuspension";
import { PeriodsSection } from "../../../../shared/components/PeriodSelectionForm/PeriodsSection";
import { OrderType } from "../../../../store/type";
import { DateString } from "../../../../shared";

export const Suspension = () => {
    const {
        navigate,
        ROUTES,
        PERSONA,
        PERIOD_TYPE,
        store,
        updateStore,
        addOrder,
        ordersDate,
        updateOrder,
        removeOrder
    } = useSuspension();

    return (

        <div id="suspension" className="tab-content">
            <h2>Периоды приостановок выплат</h2>

            <div className="simplified-section">
                <div className="checkbox-group">
                    <input
                        type="checkbox"
                        id="suspensionPeriodCheck"
                        checked={store.is_suspension}
                        onChange={(e) => updateStore('is_suspension', e.target.checked)}
                    />
                    <label htmlFor="suspensionPeriodCheck">Есть периоды приостановок выплат</label>
                </div>

                {store.is_suspension && (
                    <PeriodsSection persona={PERSONA.adult} typePeriod={PERIOD_TYPE.stop_payment} />
                )}
            </div>




            {store.is_adult && (
                <>

                    <div className="simplified-section">
                        <div className="checkbox-group">
                            <input
                                type="checkbox"
                                id="employmentPeriodCheck"
                                checked={store.is_employment}
                                onChange={(e) => updateStore('is_employment', e.target.checked)}
                            />
                            <label htmlFor="employmentPeriodCheck">Есть периоды приостановок выплат в связи с трудоустройством</label>
                        </div>

                        {store.is_employment && (
                            <PeriodsSection persona={PERSONA.adult} typePeriod={PERIOD_TYPE.employment} />
                        )}
                    </div>


                    <div className="simplified-section">
                        <div className="checkbox-group">
                            <input
                                type="checkbox"
                                id="inpatientPeriodCheck"
                                checked={store.is_order}
                                onChange={(e) => updateStore('is_order', e.target.checked)}
                            />
                            <label htmlFor="inpatientPeriodCheck">Есть обращения с заявлением на получение РСД до ГСС</label>
                        </div>

                        {store.is_order && (
                            <>
                                {ordersDate?.map((order, idx) => (
                                    <>
                                        <OrdereGssItem
                                            key={order.id}
                                            orderId={order.id}
                                            index={idx + 1}
                                            orderData={order}
                                            onUpdateOrder={updateOrder}
                                            onRemoveOrder={removeOrder}
                                        />

                                    </>
                                ))}
                                <button
                                    type="button"
                                    className="btn btn-small"
                                    onClick={() => addOrder()}
                                >
                                    + Добавить обращение
                                </button>
                            </>
                        )}


                    </div>
                </>
            )}



            <div className="form-group">
                <button className="btn btn-secondary" id="backToParams" onClick={() => navigate(ROUTES.payments)}>Назад: Выплаты и периоды</button>
                <button className="btn btn-success" id="nextToPayments" onClick={() => navigate(ROUTES.results)}>Далее: Результаты</button>
            </div>
        </div>

    )
}


const OrdereGssItem = (
    {
        orderId,
        index,
        orderData,
        onUpdateOrder,
        onRemoveOrder
    }: {
        orderId: number;
        index: number;
        orderData: OrderType;
        onUpdateOrder: (orderId: number, date: DateString) => void;
        onRemoveOrder: (orderId: number) => void;
    }) => {

    return (
        <div className="container date-period">
            <div className="recalculation-header">
                <h4>Заявление {index}</h4>
                <button
                    type="button"
                    className="remove-period"
                    onClick={() => onRemoveOrder(orderId)}
                >Удалить перерасчет</button>
            </div>
            <div className="grid-4">
                <div className="form-group">
                    <label>Дата заявления *</label>
                    <input
                        type="date"
                        className="order-date"
                        required
                        value={orderData?.date || ''}
                        onChange={(e) => onUpdateOrder(orderId, e.target.value)}
                    />
                </div>
            </div>
        </div>
    )
}
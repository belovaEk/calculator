
import { usePayments } from "../hooks/usePayments";
import { ROUTES } from "../../../../shared";
import { Payment } from "./Payment";

export const Payments = () => {

    const {
        store,
        updateStore,
        navigate,
        payments,
        addPaymet,
        updatePayment,
        removePayment,
        PAYMENT_TYPE
    } = usePayments();

    return (
        <>
            {/* Вкладка выплат и периодов */}
            <div id="payments" className="tab-content">
                <div className="section">
                    <h2>Выплаты и периоды их получения</h2>


                    {store.is_adult && (
                        <div className="grid">
                            <div className="form-group">
                                <label htmlFor="paymentChangeDate">Дата последнего изменния вида пенсии *</label>
                                <input
                                    id="paymentChangeDate"
                                    type="date"
                                    value={store.change_last_date}
                                    onChange={(e) => updateStore('change_last_date', e.target.value)}
                                    required
                                />
                            </div>
                        </div>
                    )}



                    <div id="paymentsContainer">
                        {payments.map((payment, index) => (
                            <Payment
                                id={payment.id}
                                index={index + 1}
                                paymentData={payment}
                                onUpdate={updatePayment}
                                onRemove={removePayment}
                            />
                        ))}
                    </div>

                    <div className="form-group">
                        <button
                            className="btn addPayment-btn"
                            id="addPension"
                            onClick={() => addPaymet(PAYMENT_TYPE.pension.raw)}
                        >+ Добавить пенсию</button>

                        {store.is_adult && (
                            <div style={{display: "inline-block"}}>
                                <button
                                    className="btn addPayment-btn"
                                    id="addEdv"
                                    onClick={() => addPaymet(PAYMENT_TYPE.edv.raw)}
                                >+ Добавить ЕДВ+НСУ</button>

                                <button
                                    className="btn addPayment-btn"
                                    id="addPension"
                                    onClick={() => addPaymet(PAYMENT_TYPE.egdv.raw)}
                                >+ Добавить ЕГДВ</button>

                                <button
                                    className="btn addPayment-btn"
                                    id="addPension"
                                    onClick={() => addPaymet(PAYMENT_TYPE.edk.raw)}
                                >+ Добавить ЕДК</button>

                                <button
                                    className="btn addPayment-btn"
                                    id="addPension"
                                    onClick={() => addPaymet(PAYMENT_TYPE.housing.raw)}
                                >+ Добавить ЖКУ</button>
                            </div>
                        )}

                    </div>

                    {/* <h3>Список всех выплат</h3>
                    <div id="paymentsList" className="payment-list">
                    </div> */}


                </div>




                <div className="form-group">
                    <button className="btn btn-secondary" id="backToBasic" onClick={() => navigate(ROUTES.inpatient)}>Назад: Размещение в стационарах</button>
                    <button className="btn btn-success" id="nextToResults" onClick={() => navigate(ROUTES.suspension)}>Далее: Приостановка выплат</button>
                </div>
            </div>


        </>
    )
}
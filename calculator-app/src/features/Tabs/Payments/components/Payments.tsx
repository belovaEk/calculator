
import { usePayments } from "../hooks/usePayments";
import { ROUTES } from "../../../../shared";
import { Payment } from "./Payment";

export const Payments = () => {

    const {
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


                    <div className="form-group">
                        <button
                            className="btn"
                            id="addPension"
                            onClick={() => addPaymet(PAYMENT_TYPE.pension.raw)}
                        >+ Добавить пенсию</button>

                        {/* <button className="btn" id="addEdv">+ Добавить ЕДВ</button>
                        <button className="btn" id="addEgdv">+ Добавить ЕГДВ</button>
                        <button className="btn" id="addHousing">+ Добавить ЖКУ</button>
                        <button className="btn btn-secondary" id="addCustom">+ Добавить другую выплату</button> */}
                        
                    </div>

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
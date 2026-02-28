
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

                    {/* <div className="grid">
                        <div className="form-group">
                            <label>Дата первичного назначения пенсии в Москве*</label>
                            <input
                                type="date"
                                className="payment-end"
                                value={store.date_of_the_initial_appointment_of_the_spv}
                                onChange={(e) => updateStore('date_of_the_initial_appointment_of_the_spv', e.target.value)}
                                required
                            />
                        </div>
                    </div> */}


                    {/* <div className="info-box warning">
                        <p><strong>Важно:</strong> При расчете РСД на январь используются значения пенсий и ЕДВ на декабрь
                            предыдущего года. Для правильного расчета необходимо заполнить раздельные значения.</p>
                        <p><strong>Примечание:</strong> Поле "Размер на январь" не является обязательным. Если не заполнено,
                            будет использоваться значение на декабрь.</p>
                    </div> */}

                    <div className="form-group">
                        {/* <button className="btn btn-success" id="autoFillAll">🔄 Автозаполнить все выплаты</button> */}
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
                        {/* <Payment
                        id={1} 
                        index={1}
                            type="pension"
                            paymentData={{
                                id: 1,
                                type: 'pension',
                                categoria:  '',
                                DN: '',
                                DK: '',
                                paymentAmount: 0,
                                is_Moscow: false,
                                is_suspension: false,}
                                }
                                onUpdate={()=> console.log()}
                                onRemove={()=> console.log()}
                        /> */}
                    </div>

                    {/* <h3>Список всех выплат</h3>
                    <div id="paymentsList" className="payment-list">
                    </div> */}


                </div>




                <div className="form-group">
                    <button className="btn btn-secondary" id="backToBasic" onClick={() => navigate(ROUTES.inpatient)}>Назад: Размещение в стационарах</button>
                    <button className="btn btn-success" id="nextToResults" onClick={() => navigate(ROUTES.results)}>Далее: Расчет</button>
                </div>
            </div>


        </>
    )
}
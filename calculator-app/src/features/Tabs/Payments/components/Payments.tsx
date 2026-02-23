import CustomPayment from "./paymentsTypes/Custom";
import EdvPayment from "./paymentsTypes/Edv";
import EgdPayment from "./paymentsTypes/Egd";
import HousingPayment from "./paymentsTypes/Housing";
import PensionPayment from "./paymentsTypes/Pension"

export const Payments = () => {
    return (
        <>
            {/* Вкладка выплат и периодов */}
            <div id="payments" className="tab-content">
                <div className="section">
                    <h2>Выплаты и периоды их получения</h2>

                    <div className="info-box warning">
                        <p><strong>Важно:</strong> При расчете РСД на январь используются значения пенсий и ЕДВ на декабрь
                            предыдущего года. Для правильного расчета необходимо заполнить раздельные значения.</p>
                        <p><strong>Примечание:</strong> Поле "Размер на январь" не является обязательным. Если не заполнено,
                            будет использоваться значение на декабрь.</p>
                    </div>

                    <div className="form-group">
                        <button className="btn btn-success" id="autoFillAll">🔄 Автозаполнить все выплаты</button>
                        <button className="btn" id="addPension">+ Добавить пенсию</button>
                        <button className="btn" id="addEdv">+ Добавить ЕДВ</button>
                        <button className="btn" id="addEgdv">+ Добавить ЕГДВ</button>
                        <button className="btn" id="addHousing">+ Добавить ЖКУ</button>
                        <button className="btn btn-secondary" id="addCustom">+ Добавить другую выплату</button>
                    </div>

                    <div id="paymentsContainer">
                        {/* Выплаты будут добавляться динамически */}
                    </div>

                    <PensionPayment />
                    <EdvPayment />
                    <EgdPayment />
                    <HousingPayment />
                    <CustomPayment />

                    <h3>Список всех выплат</h3>
                    <div id="paymentsList" className="payment-list">
                        {/* Список выплат будет отображаться здесь */}
                    </div>


                </div>




                <div className="form-group">
                    <button className="btn btn-secondary" id="backToBasic">Назад: Основные данные</button>
                    <button className="btn btn-success" id="nextToResults">Далее: Расчет</button>
                </div>
            </div>


        </>
    )
}
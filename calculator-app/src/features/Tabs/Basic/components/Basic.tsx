import { useBasic } from "../hooks/useBasic";
import { PeriodsSection } from "../../../../shared/components/PeriodSelectionForm/PeriodsSection";

export const Basic = () => {

    const {
        navigate,
        store,
        updateStore,
        isBreadwinner,
        updateIsBreadwinner,
        ROUTES,
        PERIOD_TYPE,
        PERSONA,
    } = useBasic();


    return (
        <>
            {/* Вкладка основных данных */}
            <div id="basic" className="tab-content">
                <div className="section">
                    <h2>Основные данные получателя</h2>

                    <div className="simplified-section">

                        {/* ребенок / взрослый */}
                        <div className="radio-group">
                            <div className="radio-item">
                                <input
                                    id="children"
                                    type="radio"
                                    name="ageGroupCheck"
                                    checked={store.is_adult === false}
                                    onChange={() => updateStore('is_adult', false)}
                                    defaultChecked
                                />
                                <label htmlFor="children">Ребенок</label>
                            </div>
                            <div className="radio-item">
                                <input
                                    id="adult"
                                    type="radio"
                                    name="ageGroupCheck"
                                    checked={store.is_adult === true}
                                    onChange={() => updateStore('is_adult', true)}
                                />
                                <label htmlFor="adult">Взрослый</label>
                            </div>
                        </div>

                        <div className="grid">

                            {/* дата рождения */}
                            <div className="form-group">
                                <label htmlFor="birthDate">Дата рождения *</label>
                                <input
                                    type="date"
                                    id="birthDate"
                                    onChange={(e) => updateStore('date_of_birth', e.target.value)}
                                    required />
                            </div>

                            {/* <div className="form-group" id="applicationDateGroup">
                                <label htmlFor="applicationDate">Дата заявления *</label>
                                <input type="date" id="applicationDate" required />
                            </div> */}

                            {/* <div className="form-group" id="autoAssignmentDateGroup" style={{ display: 'none' }}>
                                <label htmlFor="autoAssignmentDate">Дата автоматического назначения *</label>
                                <input type="date" id="autoAssignmentDate" />
                            </div> */}

                            {/* <div className="form-group">
                                <label htmlFor="gssApplicationDate">Дата заявления на ГСС (если отличается)</label>
                                <input type="date" id="gssApplicationDate" />
                                <div className="days-info">Оставьте пустым, если заявление на ГСС не подавалось</div>
                            </div> */}

                        </div>

                        <div className="checkbox-group">
                            <input
                                type="checkbox"
                                id="transferredCheck"
                                checked={store.is_payment_transferred}
                                onChange={(e) => updateStore('is_payment_transferred', e.target.checked)}
                            />
                            <label htmlFor="transferredCheck">Пенсия была переведена из другого региона</label>
                        </div>

                        {store.is_payment_transferred && (
                            <div className="info-box">
                                <div className="checkbox-group">
                                    <input
                                        type="checkbox"
                                        id="transferredCheckGetPSDFSDLM"
                                        checked={store.is_get_PSD_FSD_last_mounth_payment_trasferred}
                                        onChange={(e) => updateStore('is_get_PSD_FSD_last_mounth_payment_trasferred', e.target.checked)}
                                    />
                                    <label htmlFor="transferredCheckGetPSDFSDLM">Получал РСД или ФСД в предыдщуем месяце</label>
                                </div>
                                <div className="checkbox-group">
                                    <input
                                        type="checkbox"
                                        id="transferredCheckGetPSDFSDNow"
                                        checked={store.is_Not_get_PSD_FSD_now_payment_trasferred}
                                        onChange={(e) => updateStore('is_Not_get_PSD_FSD_now_payment_trasferred', e.target.checked)}
                                    />
                                    <label htmlFor="transferredCheckGetPSDFSDNow">В текущее время не получает РСД или ФСД в другом регионе</label>
                                </div>
                            </div>
                        )}

                        {!store.is_adult && (
                            <>
                                <div className="checkbox-group">
                                    <input
                                        type="checkbox"
                                        id="registrationPeriodChildrenCheck"
                                        checked={store.is_there_a_registration_in_moscow}
                                        onChange={(e) => updateStore('is_there_a_registration_in_moscow', e.target.checked)}
                                    />
                                    <label htmlFor="registrationPeriodChildrenCheck">Есть периоды регистрации в Москве</label>
                                </div>

                                {store.is_there_a_registration_in_moscow && (
                                    <PeriodsSection persona={PERSONA.children} typePeriod={PERIOD_TYPE.registration} />
                                )}
                            </>
                        )}
                    </div>

                    <div>
                        {!store.is_adult && (
                            <>
                                <h3>Законный представитель / кормилец</h3>
                                <div className="simplified-section">


                                    <div className="checkbox-group">
                                        <input
                                            type="checkbox"
                                            id="registrationPeriodLegalCheck"
                                            checked={store.is_there_a_registration_in_moscow_of_the_legal_representative}
                                            onChange={(e) => updateStore('is_there_a_registration_in_moscow_of_the_legal_representative', e.target.checked)}
                                        />
                                        <label htmlFor="registrationPeriodLegalCheck">Есть периоды регистрации в Москве законного представителя</label>
                                    </div>

                                    {store.is_there_a_registration_in_moscow_of_the_legal_representative && (
                                        <PeriodsSection persona={PERSONA.legal_representative} typePeriod={PERIOD_TYPE.registration} />
                                    )}

                                    <div className="checkbox-group">
                                        <input
                                            type="checkbox"
                                            id="breadwinnerCheck"
                                            checked={isBreadwinner}
                                            onChange={(e) => updateIsBreadwinner(e.target.checked)}
                                        />
                                        <label htmlFor="breadwinnerCheck">Потеря кормильца</label>
                                    </div>

                                    {isBreadwinner && (
                                        <>
                                            <div className="info-box warning">
                                                <div className="grid">
                                                    <div className="form-group">
                                                        <label htmlFor="date_of_death_of_the_breadwinner">Дата смерти *</label>
                                                        <input
                                                            type="date"
                                                            id="date_of_death_of_the_breadwinner"
                                                            onChange={(e) => updateStore('date_of_death_of_the_breadwinner', e.target.value)}
                                                            required />
                                                    </div>
                                                </div>
                                            </div>

                                            <div className="checkbox-group">
                                                <input
                                                    type="checkbox"
                                                    id="registrationPeriodBreadwinnerCheck"
                                                    checked={store.is_there_a_registration_in_moscow_of_the_breadwinner}
                                                    onChange={(e) => updateStore('is_there_a_registration_in_moscow_of_the_breadwinner', e.target.checked)}
                                                />
                                                <label htmlFor="registrationPeriodBreadwinnerCheck">Есть периоды регистрации в Москве кормильца</label>
                                            </div>

                                            {store.is_there_a_registration_in_moscow_of_the_breadwinner && (
                                                <PeriodsSection persona={PERSONA.breadwinner} typePeriod={PERIOD_TYPE.registration} />
                                            )}

                                        </>
                                    )}
                                </div>

                            </>
                        )}











                    </div>

                    {/* <div id="registrationSummary" style={{ marginBottom: '15px', padding: '10px', backgroundColor: '#e8f4fc', borderRadius: '5px' }}>
                        <strong>Итоговая продолжительность регистрации:</strong> <span id="totalRegistrationDuration">0 лет 0 месяцев 0 дней</span>
                        <br />
                        <strong>Дата достижения 10 лет регистрации:</strong> <span id="tenYearRegistrationDate">Не достигнуто</span>
                    </div> */}

                    {/* <div className="info-box">
                        <p><strong>Текущие параметры ГСС и ПМП:</strong></p>
                        <div id="currentParamsInfo"></div>
                    </div> */}
                </div>


                <div className="form-group">
                    <button className="btn btn-secondary" id="backToParams" onClick={() => navigate(ROUTES.params)}>Назад: Параметры</button>
                    <button className="btn btn-success" id="nextToPayments" onClick={() => navigate(ROUTES.inpatient)}>Далее: Размещение в стационарах</button>
                </div>
            </div>


        </>
    )
}
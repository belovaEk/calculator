import { useBasic } from "../hooks/useBasic";
import { PeriodsSection } from "../../../../shared/components/PeriodSelectionForm/PeriodsSection";

export const Basic = () => {

    const {
        navigate,
        store,
        updateStore,
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

                        {!store.is_adult && (
                            <>
                                <div className="checkbox-group">
                                    <input
                                        type="checkbox"
                                        id="registrationPerioChildrenCheck"
                                        checked={store.is_there_a_registration_in_moscow_of_the_child}
                                        onChange={(e) => updateStore('is_there_a_registration_in_moscow_of_the_child', e.target.checked)}
                                    />
                                    <label htmlFor="registrationPerioChildrenCheck">Есть периоды регистрации в Москве ребенка</label>
                                </div>

                                {store.is_there_a_registration_in_moscow_of_the_child && (
                                    <PeriodsSection persona={PERSONA.children} typePeriod={PERIOD_TYPE.registration} />
                                )}


                                <h3>Законный представитель / кормилец</h3>

                                <div className="radio-group">
                                    <div className="radio-item">
                                        <input
                                            id="legal_representative"
                                            type="radio"
                                            name="representativeCheck"
                                            checked={store.is_legal_representative === true}
                                            onChange={() => updateStore('is_legal_representative', true)}
                                            defaultChecked
                                        />
                                        <label htmlFor="legal_representative">Законный представитель</label>
                                    </div>
                                    <div className="radio-item">
                                        <input
                                            id="breadwinner"
                                            type="radio"
                                            name="representativeCheck"
                                            checked={store.is_legal_representative === false}
                                            onChange={() => updateStore('is_legal_representative', false)}
                                        />
                                        <label htmlFor="breadwinner">Кормилец</label>
                                    </div>
                                </div>

                                {!store.is_legal_representative && (
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
                                )}

                                <div className="checkbox-group">
                                    <input
                                        type="checkbox"
                                        id="registrationPeriodLegalCheck"
                                        checked={store.is_there_a_registration_in_moscow_of_the_breadwinner_or_legal_representative}
                                        onChange={(e) => updateStore('is_there_a_registration_in_moscow_of_the_breadwinner_or_legal_representative', e.target.checked)}
                                    />
                                    <label htmlFor="registrationPeriodLegalCheck">Есть периоды регистрации в Москве законного представителя или кормильца</label>
                                </div>

                                {store.is_there_a_registration_in_moscow_of_the_breadwinner_or_legal_representative && (
                                    <PeriodsSection persona={PERSONA.representative} typePeriod={PERIOD_TYPE.registration} />
                                )}
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
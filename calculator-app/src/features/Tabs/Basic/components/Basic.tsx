import { useBasic } from "../hooks/useBasic";
import { ROUTES } from "../../../../shared/constants";

export const Basic = () => {

    const {
        navigate,
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
                                    value="false"
                                    defaultChecked
                                />
                                <label htmlFor="children">Ребенок</label>
                            </div>
                            <div className="radio-item">
                                <input
                                    id="adult"
                                    type="radio"
                                    name="ageGroupCheck"
                                    value="true"
                                />
                                <label htmlFor="adult">Взрослый</label>
                            </div>
                        </div>

                        <div className="grid">

                            {/* дата рождения */}
                            <div className="form-group">
                                <label htmlFor="birthDate">Дата рождения *</label>
                                <input type="date" id="birthDate" required />
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
                            <input type="checkbox" id="registrationPeriodsCheck" />
                            <label htmlFor="registrationPeriodsCheck">Есть периоды регистрации в Москве</label>
                        </div>

                        <div id="registrationSection">
                            <div className="form-group">
                                <h3>Периоды регистрации в Москве</h3>
                                <div className="info-box warning">
                                    <p><strong>Важно:</strong> Укажите все периоды регистрации в Москве. Общая
                                        продолжительность регистрации должна быть не менее 10 лет для получения ГСС.</p>
                                </div>

                                <div id="registrationPeriodsContainer" className="registration-periods-container">
                                    {/* Периоды регистрации будут добавляться динамически */}
                                </div>

                                <button className="btn" id="addRegistrationPeriod">+ Добавить период регистрации</button>

                                <div id="registrationSummary" style={{ marginTop: '15px', padding: '10px', backgroundColor: '#e8f4fc', borderRadius: '5px' }}>
                                    <strong>Итоговая продолжительность регистрации:</strong> <span id="totalRegistrationDuration">0 лет 0 месяцев 0 дней</span>
                                    <br />
                                    <strong>Дата достижения 10 лет регистрации:</strong> <span id="tenYearRegistrationDate">Не достигнуто</span>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div className="info-box">
                        <p><strong>Текущие параметры ГСС и ПМП:</strong></p>
                        <div id="currentParamsInfo"></div>
                    </div>
                </div>

                <div className="form-group">
                    <button className="btn btn-secondary" id="backToParams" onClick={() => navigate(ROUTES.params)}>Назад: Параметры</button>
                    <button className="btn btn-success" id="nextToPayments" onClick={() => navigate(ROUTES.payments)}>Далее: Выплаты и периоды</button>
                </div>
            </div>

            <template id="registrationPeriodTemplate">
                <div className="registration-period">
                    <div className="payment-header">
                        <div className="payment-title">Период регистрации <span className="period-number">1</span></div>
                        <button className="remove-period" type="button">Удалить период</button>
                    </div>

                    <div className="payment-dates">
                        <div className="form-group">
                            <label>Дата начала регистрации *</label>
                            <input type="date" className="period-start" required />
                        </div>

                        <div className="form-group">
                            <label>Дата окончания регистрации *</label>
                            <input type="date" className="period-end" required />
                        </div>
                    </div>

                    <div className="date-options">
                        <div className="date-option-group">
                            <input type="checkbox" className="current-date" />
                            <label className="date-option-label">По настоящее время</label>
                        </div>
                        <div className="date-option-group">
                            <input type="checkbox" className="indefinite" />
                            <label className="date-option-label">Непрерывно (до прекращения)</label>
                        </div>
                    </div>
                </div>
            </template>
        </>
    )
}
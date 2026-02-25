import { useResults } from "../hooks/useResults";
import { ROUTES } from "../../../../shared/constants";

export const Results = () => {

    const {
        navigate,
    } = useResults();

    return (
        <>
            {/* Вкладка результатов расчета */}
            <div id="results" className="tab-content">
                <div className="section">
                    <h2>Результаты расчета</h2>

                    <div className="info-box">
                        <p><strong>Информация о получателе:</strong> <span id="resultPersonInfo"></span></p>
                        <p><strong>Порядок назначения:</strong> <span id="resultAppointmentOrder"></span></p>
                        <p><strong>Общая продолжительность регистрации в Москве:</strong> <span id="resultRegDuration"></span></p>
                        <p><strong>Дата достижения 10-летнего срока регистрации:</strong> <span id="result10YearDate"></span></p>
                        <p id="resultApplicationDateInfo"><strong>Дата заявления:</strong> <span id="resultApplicationDate"></span></p>
                        <p id="resultAutoAssignmentDateInfo" style={{ display: 'none' }}><strong>Дата автоматического назначения:</strong> <span id="resultAutoAssignmentDate"></span></p>
                        <p><strong>Дата заявления на ГСС:</strong> <span id="resultGssApplicationDate"></span></p>
                        <p id="resultGssStartDateInfo"><strong>Дата начала ГСС (1 число месяца, следующего за заявлением на ГСС):</strong> <span id="resultGssStartDate"></span></p>
                    </div>

                    <div id="calculationErrors" className="info-box error hidden">
                        <h3>Ошибки в данных</h3>
                        <div id="errorsList"></div>
                    </div>

                    <div id="calculationWarnings" className="info-box warning hidden">
                        <h3>Предупреждения</h3>
                        <div id="warningsList"></div>
                    </div>

                    <h3>Сводная таблица периодов с одинаковой суммой РСД</h3>
                    <div id="consolidatedResults"></div>

                    <h3>Детализированный расчет по дням</h3>
                    <div id="detailedResults"></div>

                    <div className="result-section">
                        <h3>Итоги расчета</h3>
                        <p><strong>Общая сумма положенной доплаты за все периоды:</strong> <span id="totalPayment" className="highlight">0.00 руб.</span></p>
                        <p><strong>Общая недополученная сумма (за 3 года до даты заявления):</strong> <span id="totalUnderpayment" className="highlight">0.00 руб.</span></p>
                        <p><strong>Дата расчета:</strong> <span id="calculationDate"></span></p>
                    </div>
                </div>

                <div className="form-group">
                    <button className="btn btn-secondary" id="backToPayments" onClick={()=> navigate(ROUTES.payments)}>Назад: Выплаты и периоды</button>
                    <button className="btn" id="recalculate">Пересчитать</button>
                    <button className="btn btn-success" id="printResults">Распечатать результаты</button>
                    <button className="btn btn-danger" id="resetAll">Сбросить все данные</button>
                </div>
            </div>
        </>
    )
}
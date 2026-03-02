import { useResults } from "../hooks/useResults";
import { ROUTES } from "../../../../shared/constants";
import { useEffect } from "react";

export const Results = () => {

    const {
        navigate,
        calculate,
        tableDataPmpGss,
        tableDataPmpGssRsd,
        resetStore,
        handlePrint,
        message,
        isLoading
    } = useResults();

    useEffect(() => {
        calculate();
    }, [calculate]);

    return (
        <>
            <div id="results" className="tab-content">
                <div className="section">
                    <h2>Результаты расчета</h2>

                    {isLoading ? (
                        <div className="loading-spinner">
                            <div className="spinner"></div>
                            <p>Выполняется расчет...</p>
                        </div>
                    ) : (
                        <>
                            {/* <div className="info-box">
                                <p><strong>Информация о получателе:</strong> <span id="resultPersonInfo"></span></p>
                                <p><strong>Порядок назначения:</strong> <span id="resultAppointmentOrder"></span></p>
                                <p><strong>Общая продолжительность регистрации в Москве:</strong> <span id="resultRegDuration"></span></p>
                                <p><strong>Дата достижения 10-летнего срока регистрации:</strong> <span id="result10YearDate"></span></p>
                                <p id="resultApplicationDateInfo"><strong>Дата заявления:</strong> <span id="resultApplicationDate"></span></p>
                                <p id="resultAutoAssignmentDateInfo" style={{ display: 'none' }}><strong>Дата автоматического назначения:</strong> <span id="resultAutoAssignmentDate"></span></p>
                                <p><strong>Дата заявления на ГСС:</strong> <span id="resultGssApplicationDate"></span></p>
                                <p id="resultGssStartDateInfo"><strong>Дата начала ГСС (1 число месяца, следующего за заявлением на ГСС):</strong> <span id="resultGssStartDate"></span></p>
                            </div> */}

                            <div id="calculationErrors" className="info-box error hidden">
                                <h3>Ошибки в данных</h3>
                                <div id="errorsList"></div>
                            </div>

                            {message && (
                                <div id="calculationWarnings" className="info-box warning">
                                    <h3>Предупреждения</h3>
                                    <div id="warningsList">{message}</div>
                                </div>
                            )}

                            {tableDataPmpGss && tableDataPmpGss.length > 0 ? (
                                <>
                                    <h3>Сводная таблица периодов ПМП и ГСС</h3>
                                    <div id="consolidatedResults_GssPmp">
                                        <table className="params-table">
                                            <thead>
                                                <tr className="grid-header">
                                                    <th className="highlighting-header">Вид выплаты</th>
                                                    <th>Вид пенсии</th>
                                                    <th>Дата начала</th>
                                                    <th>Дата конца</th>
                                                </tr>
                                            </thead>
                                            <tbody>
                                                {tableDataPmpGss.map((row, index) => (
                                                    <tr className="grid-header" key={index}>
                                                        <td>
                                                            {row.paymentType}
                                                        </td>
                                                        <td>{row.pensionType}</td>
                                                        <td>{row.startDate}</td>
                                                        <td>{row.endDate}</td>
                                                    </tr>
                                                ))}
                                            </tbody>
                                        </table>
                                    </div>
                                </>
                            ) : !message && (
                                <div className="info-box warning">
                                    <p>Нет данных для отображения. Возможно, не все обязательные поля заполнены или <b>выбраны года раньше 2020</b></p>
                                </div>
                            )}

                            {tableDataPmpGssRsd && tableDataPmpGssRsd.length > 0 ? (
                                <>
                                    <h3>Детализированный расчет</h3>
                                    <div id="consolidatedResults_Rsd">
                                        <table className="params-table">
                                            <thead>
                                                <tr className="grid-header">
                                                    <th className="highlighting-header">Вид выплаты</th>
                                                    <th>Дата начала</th>
                                                    <th>Дата конца</th>
                                                    <th>Сумма рсд ежемесячно руб/мес</th>
                                                </tr>
                                            </thead>
                                            <tbody>
                                                {tableDataPmpGssRsd.map((row, index) => (
                                                    <tr className="grid-header" key={index}>
                                                        <td>{row.paymentType}</td>
                                                        <td>{row.startDate}</td>
                                                        <td>{row.endDate}</td>
                                                        <td>{row.amount}</td>
                                                    </tr>
                                                ))}
                                            </tbody>
                                        </table>
                                    </div></>
                            ) : message && (
                                <div className="info-box warning">
                                    <p>Нет данных для отображения. Возможно, не все обязательные поля заполнены.</p>
                                </div>
                            )}

                            {/* <h3>Детализированный расчет по дням</h3>
                            <div id="detailedResults"></div> */}

                            {/* <div className="result-section">
                                <h3>Итоги расчета</h3>
                                <p><strong>Общая сумма положенной доплаты за все периоды:</strong> <span id="totalPayment" className="highlight">0.00 руб.</span></p>
                                <p><strong>Общая недополученная сумма (за 3 года до даты заявления):</strong> <span id="totalUnderpayment" className="highlight">0.00 руб.</span></p>
                                <p><strong>Дата расчета:</strong> <span id="calculationDate"></span></p>
                            </div> */}
                        </>
                    )}
                </div>

                <div className="form-group">
                    <button
                        className="btn btn-secondary"
                        id="backToPayments"
                        onClick={() => navigate(ROUTES.payments)}
                        disabled={isLoading}
                    >
                        Назад: Выплаты и периоды
                    </button>
                    <button
                        className="btn"
                        id="recalculate"
                        onClick={() => calculate()}
                        disabled={isLoading}
                    >
                        {isLoading ? 'Расчет...' : 'Пересчитать'}
                    </button>
                    <button
                        className="btn btn-success"
                        id="printResults"
                        onClick={() => handlePrint()}
                        disabled={isLoading}
                    >
                        Распечатать результаты
                    </button>
                    <button
                        className="btn btn-danger"
                        id="resetAll"
                        onClick={() => resetStore()}
                        disabled={isLoading}
                    >
                        Сбросить все данные
                    </button>
                </div>
            </div>
        </>
    )
}
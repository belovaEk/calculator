
export const Params = () => {
    return (
        <>
            {/* Вкладка параметров ГСС и ПМП */}
            <div id="params" className="tab-content active">
                <div className="section">
                    <h2>Установка параметров ГСС и ПМП по годам</h2>

                    <div className="info-box">
                        <p><strong>Инструкция:</strong> Укажите значения Городского социального стандарта (ГСС) и
                            Прожиточного минимума пенсионера (ПМП) в рублях для каждого года.</p>
                    </div>

                    <table className="params-table">
                        <thead>
                            <tr>
                                <th className="year-header">Год</th>
                                <th>ГСС (руб.)</th>
                                <th>ПМП (руб.)</th>
                            </tr>
                        </thead>
                        <tbody id="paramsTableBody">
                            {/* Данные будут заполнены через JavaScript */}
                        </tbody>
                    </table>

                    <div className="form-group" style={{ marginTop: '20px' }}>
                        <button className="btn" id="resetParams">Сбросить к значениям по умолчанию</button>
                        <button className="btn btn-success" id="saveParams">Сохранить параметры</button>
                    </div>
                </div>

                <div className="form-group">
                    <button className="btn btn-success" id="nextFromParams">Далее: Основные данные</button>
                </div>
            </div>
        </>
    )
}
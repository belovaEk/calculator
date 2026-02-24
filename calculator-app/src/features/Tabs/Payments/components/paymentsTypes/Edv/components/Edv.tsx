import { EDV_CATEGORIES } from "../../../../../../../shared/constants"

export const EdvPayment = () => {

    const categoryEntries = Object.entries(EDV_CATEGORIES);
    
    return (
        // {/* Шаблон для ЕДВ */}
        <div id="edvTemplate">
            <div className="payment-entry">
                <div className="payment-header">
                    <div className="payment-title">ЕДВ <span className="payment-number">1</span></div>
                    <button className="remove-payment" type="button">Удалить выплату</button>
                </div>

                <div className="payment-dates">
                    <div className="form-group">
                        <label>Дата начала выплаты *</label>
                        <input type="date" className="payment-start" required />
                    </div>

                    <div className="form-group">
                        <label>Дата окончания выплаты *</label>
                        <input type="date" className="payment-end" required />
                    </div>
                </div>

                <div className="date-options">
                    <div className="date-option-group">
                        <input type="checkbox" className="current-date" />
                        <label className="date-option-label">По настоящее время</label>
                    </div>
                    <div className="date-option-group">
                        <input type="checkbox" className="indefinite" />
                        <label className="date-option-label">Бессрочно</label>
                    </div>
                </div>

                <div className="form-group">
                    <label>Тип выплаты</label>
                    <input type="text" className="payment-type" value="Ежемесячная денежная выплата (ЕДВ)" readOnly />
                </div>

                <div className="form-group">
                    <label>Группа инвалидности *</label>
                    <select className="edv-group" required>
                        <option value="">Выберите группу</option>
                        ({categoryEntries.map(([key, value]) => (
                            <option key={key} value={value}>
                                {value}
                            </option>
                        ))})
                    </select>
                </div>

                <div className="amount-period">
                    <div className="form-group">
                        <label>Размер на декабрь (руб.) *</label>
                        <input type="number" className="payment-amount-dec" min="0" step="0.01" required />
                        <div className="period-label">Используется для расчета января</div>
                    </div>

                    <div className="form-group">
                        <label>Размер на январь (руб.)</label>
                        <input type="number" className="payment-amount-jan" min="0" step="0.01" />
                        <div className="period-label">Если не заполнено, используется значение на декабрь</div>
                    </div>
                </div>

                <div className="grid-4">
                    <div className="checkbox-group">
                        <input type="checkbox" className="full-state-support-period" />
                        <label>Полное государственное обеспечение</label>
                    </div>
                    <div className="form-group">
                        <button type="button" className="btn btn-secondary btn-sm auto-fill-btn" style={{ padding: '8px 12px', fontSize: '14px' }}>Автозаполнение</button>
                    </div>
                </div>
            </div>
        </div>
    )
}
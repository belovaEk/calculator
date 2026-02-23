export const EgdPayment = () => {
    return (
        // {/* Шаблон для ЕГДВ */}
            <div id="egdTemplate">
                <div className="payment-entry">
                    <div className="payment-header">
                        <div className="payment-title">ЕГДВ <span className="payment-number">1</span></div>
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
                        <label style={{ color: 'red' }}>Тип выплаты</label>
                        <input type="text" className="payment-type" value="Ежемесячная городская денежная выплата (ЕГДВ)" readOnly />
                    </div>

                    <div className="form-group">
                        <label>Категория получателя *</label>
                        <select className="egd-category" required>
                            <option value="">Выберите категорию</option>
                            <option value="инвалиды 1 группы дети-инвалиды уход">Инвалиды 1 группы, дети-инвалиды, уход</option>
                            <option value="инвалиды с детства 2 группы сироты">Инвалиды с детства 2 группы, сироты</option>
                            <option value="пенсионеры по старости инвалиды 2 группы СПК">Пенсионеры по старости, инвалиды 2 группы, СПК</option>
                            <option value="инвалиды 3 группы">Инвалиды 3 группы</option>
                            <option value="custom">Другая (указать вручную)</option>
                        </select>
                    </div>

                    <div className="grid-4">
                        <div className="form-group">
                            <label>Размер выплаты (руб.) *</label>
                            <input type="number" className="payment-amount" min="0" step="0.01" required />
                        </div>
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
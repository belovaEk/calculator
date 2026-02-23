export const CustomPayment = () => {
    return (
        // {/* Шаблон для другой выплаты */}
            <div id="customTemplate">
                <div className="payment-entry">
                    <div className="payment-header">
                        <div className="payment-title">Другая выплата <span className="payment-number">1</span></div>
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
                        <label>Название выплаты *</label>
                        <input type="text" className="payment-title-custom" placeholder="Например: Компенсация по уходу" required />
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
                    </div>
                </div>
            </div>
    )
}
import { usePayment } from "../hooks/usePayment";

import { PaymentProps } from "./types/paymentType";
import PeriodsSection from "../../../../shared/components/PeriodSelectionForm";
import { PERSONA } from "../../../../shared/constants/people";

export const Payment = ({ id, index, paymentData, onUpdate, onRemove }: PaymentProps) => {

    const {
        PAYMENT_TYPE,
        PENSION_CATEGORIES,
        updatePayment,
        handleRemove,
        handleCurrentDate,
    } = usePayment({ id, paymentData, onUpdate, onRemove });

    return (
        <>
            <div id="pensionTemplate">
                <div className="payment-entry">
                    <div className="payment-header">
                        <div className="payment-title">{PAYMENT_TYPE[`${paymentData.type}`].display} <span className="payment-number">{index}</span></div>
                        <button
                            className="remove-payment"
                            type="button"
                            onClick={handleRemove}
                        >Удалить выплату</button>
                    </div>

                    <div className="payment-dates">
                        <div className="form-group">
                            <label>Дата начала выплаты *</label>
                            <input
                                type="date"
                                className="payment-start"
                                required
                                value={paymentData.DN}
                                onChange={(e) => updatePayment('DN', e.target.value)}
                            />
                        </div>

                        <div className="form-group">
                            <label>Дата окончания выплаты *</label>
                            <input
                                type="date"
                                className="payment-end"
                                value={paymentData.DK}
                                onChange={(e) => updatePayment('DK', e.target.value)}
                                required
                            />
                        </div>
                    </div>

                    <div className="date-options">
                        <div className="date-option-group">
                            <input
                                type="checkbox"
                                className="current-date"
                                value={paymentData.DK}
                                onChange={handleCurrentDate}
                            />
                            <label className="date-option-label">По настоящее время</label>
                        </div>
                        {/* <div className="date-option-group">
                            <input type="checkbox" className="indefinite" />
                            <label className="date-option-label">Бессрочно</label>
                        </div> */}
                    </div>

                    {paymentData.type === PAYMENT_TYPE.pension.raw && (
                        <>
                            <div className="checkbox-group">
                                <input
                                    type="checkbox"
                                    id="MoscowCheck"
                                    checked={paymentData.is_Moscow}
                                    onChange={(e) => updatePayment('is_Moscow', e.target.checked)}
                                />
                                <label htmlFor="MoscowChec">Назначена в Москве</label>
                            </div>

                            <div className="form-group">
                                <label>Вид пенсии *</label>
                                <select className="pensionType" required onChange={(e) => updatePayment('categoria', e.target.value)}>
                                    <option value="">Выберите вид пенсии</option>
                                    ({Object.entries(PENSION_CATEGORIES).map(([key, category]) => (
                                        <option key={key} value={category.raw}>{category.display}</option>
                                    ))})
                                </select>
                            </div>
                        </>
                    )}


                    <div className="form-group">
                        <label>Размер назначенной выплаты*</label>
                        <input
                            type="number"
                            className="payment-amount"
                            min="0" step="0.01"
                            value={paymentData.paymentAmount}
                            onChange={(e) => updatePayment('paymentAmount', e.target.value)}
                            required />
                    </div>


                    <div className="checkbox-group">
                        <input
                            type="checkbox"
                            id="stopPeriodCheck"
                            checked={paymentData.is_suspension}
                            onChange={(e) => updatePayment('is_suspension', e.target.checked)}
                        />
                        <label htmlFor="stopPeriodCheck">Были периоды приостановки</label>
                    </div>

                    {paymentData.is_suspension && (
                                <PeriodsSection persona="" typePeriod="приостановление выплаты" paymentId={paymentData.id}/>
                    )}

                    {/* <div className="amount-period">
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
                    </div> */}

                    {/* <div className="grid-4">
                        <div className="checkbox-group">
                            <input type="checkbox" className="is-working" />
                            <label>Работает в период выплаты</label>
                        </div>
                        <div className="checkbox-group">
                            <input type="checkbox" className="full-state-support-period" />
                            <label>Полное государственное обеспечение</label>
                        </div>
                        <div className="form-group">
                            <button type="button" className="btn btn-secondary btn-sm auto-fill-btn" style={{ padding: '8px 12px', fontSize: '14px' }}>Автозаполнение</button>
                        </div>
                    </div> */}
                </div>
            </div>
        </>
    )
}
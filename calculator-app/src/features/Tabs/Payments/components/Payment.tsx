import { usePayment } from "../hooks/usePayment";

import { PaymentProps } from "./types/paymentType";

import { RecalculationData } from "./types/paymentType";


export const Payment = ({ id, index, paymentData, onUpdate, onRemove }: PaymentProps) => {

    const {
        PAYMENT_TYPE,
        PENSION_CATEGORIES,
        updatePayment,
        handleRemove,
        handleCurrentDate,
        updateRecalculation,
        addRecalculation,
        removeRecalculation,
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
                                <label htmlFor="MoscowCheck">Назначена в Москве</label>
                            </div>

                            <div className="form-group">
                                <label>Вид пенсии *</label>
                                <select className="pensionType" required onChange={(e) => updatePayment('categoria', e.target.value)} value={paymentData.categoria}>
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
                            value={paymentData.amount}
                            onChange={(e) => updatePayment('amount', e.target.value)}
                            required />
                    </div>

                    {paymentData.categoria === PENSION_CATEGORIES.departmental.raw && (

                        <>
                            <div className="checkbox-group">
                                <input
                                    type="checkbox"
                                    id="recalculationCheck"
                                    checked={paymentData.is_recalculation}
                                    onChange={(e) => updatePayment('is_recalculation', e.target.checked)}
                                />
                                <label htmlFor="recalculationCheck">Есть перерасчет</label>
                            </div>

                            {paymentData.is_recalculation && (
                                <div id="recalculatiionContainer" className="recalculatiion-container">
                                    {paymentData.recalculation?.map((recal, idx) => (
                                        <>
                                            <DepartmentalRecalculationForm
                                                key={idx}
                                                paymentId={id}
                                                recalIndex={idx}
                                                index={idx + 1}
                                                recalData={recal}
                                                onUpdateRecalculation={updateRecalculation}
                                                onRemoveRecalculation={removeRecalculation}
                                            />

                                        </>
                                    ))}

                                    <button
                                        type="button"
                                        className="btn btn-small"
                                        onClick={addRecalculation}
                                    >
                                        + Добавить перерасчет
                                    </button>
                                </div>
                            )}
                        </>
                    )}

                </div>
            </div>
        </>
    )
}


const DepartmentalRecalculationForm = ({
    paymentId,
    recalIndex,
    index,
    recalData,
    onUpdateRecalculation,
    onRemoveRecalculation
}: {
    paymentId: number;
    recalIndex: number;
    index: number;
    recalData: RecalculationData;
    onUpdateRecalculation: (paymentId: number, recalIndex: number, field: keyof RecalculationData, value: any) => void;
    onRemoveRecalculation: (paymentId: number, recalIndex: number) => void;
}) => {

    return (
        <div className="container rec-container">
            <div className="recalculation-header">
                <h4>{index} перерасчет</h4>
                <button
                    type="button"
                    className="remove-payment"
                    onClick={() => onRemoveRecalculation(paymentId, recalIndex)}
                >Удалить перерасчет</button>
            </div>
            <div className="grid-4">
                <div className="form-group">
                    <label>Дата перерасчета *</label>
                    <input
                        type="date"
                        className="recalculation-date"
                        required
                        value={recalData?.date || ''}
                        onChange={(e) => onUpdateRecalculation(paymentId, recalIndex, 'date', e.target.value)}
                    />
                </div>
                <div className="form-group">
                    <label>Сумма *</label>
                    <input
                        type="number"
                        className="recalculation-amount"
                        min="0"
                        step="0.01"
                        value={recalData?.amount || ''}
                        onChange={(e) => onUpdateRecalculation(paymentId, recalIndex, 'amount', parseFloat(e.target.value) || 0)}
                        required
                    />
                </div>
            </div>
        </div>
    )
}
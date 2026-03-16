import { usePayment } from "../hooks/usePayment";

import { PaymentProps } from "./types/paymentType";

import { RecalculationData } from "./types/paymentType";


export const Payment = ({ id, index, paymentData, onUpdate, onRemove }: PaymentProps) => {

    const {
        store,
        PAYMENT_TYPE,
        PENSION_CATEGORIES_CHILDREN,
        PENSION_CATEGORIES_ADULT,
        updatePayment,
        handleRemove,
        handleCurrentDate,
        updateRecalculation,
        addRecalculation,
        removeRecalculation,
        addRecalculationFixAmount,
        updateRecalculationFixAmount,
        removeRecalculationFixAmount,
        PERSON_CATEGORIES
    } = usePayment({ id, paymentData, onUpdate, onRemove });


    return (
        <>
            <div id="paymentTemplate">

                <div className="payment-entry">

                    <div className="payment-header">
                        <div className="payment-title">{PAYMENT_TYPE[`${paymentData.type}`].display} <span className="payment-number">{index}</span></div>
                        <button
                            className="remove-payment"
                            type="button"
                            onClick={handleRemove}
                        >Удалить выплату</button>
                    </div>

                    {/* Дата начала и дата конца */}
                    <div>
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

                    </div>

                    {paymentData.type === PAYMENT_TYPE.egdv.raw && (
                        <div className="form-group">
                            <label>Категория граждан *</label>
                            <select className="pensionType" required onChange={(e) => updatePayment('categoria_person', e.target.value)} value={paymentData.categoria_person}>
                                <option value="">Выберите категорию</option>
                                ({Object.entries(PERSON_CATEGORIES).map(([key, category]) => (
                                    <option key={key} value={category.raw}>{category.display}</option>
                                ))})
                            </select>
                        </div>
                    )}



                    {/* Для пенсии */}
                    {paymentData.type === PAYMENT_TYPE.pension.raw && (

                        <div>

                            {/* Назначена в Москве */}
                            <div className="checkbox-group">
                                <input
                                    type="checkbox"
                                    id="MoscowCheck"
                                    checked={paymentData.is_Moscow}
                                    onChange={(e) => updatePayment('is_Moscow', e.target.checked)}
                                />
                                <label htmlFor="MoscowCheck">Назначена в Москве</label>
                            </div>

                            {/* Выбор типа пенсии для детей */}
                            {!store.is_adult && (
                                <div className="form-group">
                                    <label>Вид пенсии *</label>
                                    <select className="pensionType" required onChange={(e) => updatePayment('categoria', e.target.value)} value={paymentData.categoria}>
                                        <option value="">Выберите вид пенсии</option>
                                        ({Object.entries(PENSION_CATEGORIES_CHILDREN).map(([key, category]) => (
                                            <option key={key} value={category.raw}>{category.display}</option>
                                        ))})
                                    </select>
                                </div>
                            )}

                            {/* Выбор типа пенсии для взрослых */}
                            {store.is_adult && (
                                <div className="form-group">
                                    <label>Вид пенсии *</label>
                                    <select className="pensionType" required onChange={(e) => updatePayment('categoria', e.target.value)} value={paymentData.categoria}>
                                        <option value="">Выберите вид пенсии</option>
                                        ({Object.entries(PENSION_CATEGORIES_ADULT).map(([key, category]) => (
                                            <option key={key} value={category.raw}>{category.display}</option>
                                        ))})
                                    </select>
                                </div>
                            )}


                            {/* Пенсия была переведена из другого региона? */}
                            {(paymentData.categoria === 'insurance'
                                || paymentData.categoria === 'social'
                                || paymentData.categoria === 'gosudarstvennaya'
                                || paymentData.categoria === 'insurance_SPK'
                                || paymentData.categoria === 'social_SPK'
                                || paymentData.categoria === 'social_disability') &&
                                (
                                    <div>
                                        <div className="checkbox-group">
                                            <input
                                                type="checkbox"
                                                id="transferredCheck"
                                                checked={paymentData.is_payment_transferred}
                                                onChange={(e) => updatePayment('is_payment_transferred', e.target.checked)}
                                            />
                                            <label className="dop_check" htmlFor="transferredCheck">Пенсия была переведена из другого региона</label>
                                        </div>

                                        {paymentData.is_payment_transferred && (
                                            <div className="info-box">
                                                <div className="checkbox-group">
                                                    <input
                                                        type="checkbox"
                                                        id="transferredCheckGetPSDFSDLM"
                                                        checked={paymentData.is_get_PSD_FSD_last_mounth_payment_trasferred}
                                                        onChange={(e) => updatePayment('is_get_PSD_FSD_last_mounth_payment_trasferred', e.target.checked)}
                                                    />
                                                    <label htmlFor="transferredCheckGetPSDFSDLM">Получал РСД или ФСД в предыдщуем месяце</label>
                                                </div>
                                                <div className="checkbox-group">
                                                    <input
                                                        type="checkbox"
                                                        id="transferredCheckGetPSDFSDLY"
                                                        checked={paymentData.is_get_PSD_FSD_last_year_payment_trasferred}
                                                        onChange={(e) => updatePayment('is_get_PSD_FSD_last_year_payment_trasferred', e.target.checked)}
                                                    />
                                                    <label htmlFor="transferredCheckGetPSDFSDLY">Получал РСД или ФСД в прошлом году</label>
                                                </div>
                                                <div className="checkbox-group">
                                                    <input
                                                        type="checkbox"
                                                        id="transferredCheckGetPSDFSDNow"
                                                        checked={paymentData.is_Not_get_PSD_FSD_now_payment_trasferred}
                                                        onChange={(e) => updatePayment('is_Not_get_PSD_FSD_now_payment_trasferred', e.target.checked)}
                                                    />
                                                    <label htmlFor="transferredCheckGetPSDFSDNow">В текущее время не получает РСД или ФСД в другом регионе</label>
                                                </div>
                                            </div>
                                        )}
                                    </div>
                                )}

                            {/* {paymentData.categoria === 'insurance' &&
                                (
                                    <>
                                        <div className="checkbox-group">
                                            <label >Выерите категорию инвалидности, если гражданин инвалид *</label>
                                            <select className="invalidType" required onChange={(e) => updatePayment('invalid_categoria', e.target.value)} value={paymentData.invalid_categoria}>
                                                <option value="">Гражданин не инвалид</option>
                                                <option value="1">Инвалид 1 категории</option>
                                                <option value="2">Инвалид 2 категории</option>
                                                <option value="3">Инвалид 3 категории</option>
                                            </select>
                                        </div>
                                        <div className="grid">
                                            <div className="form-group">
                                                <label>Количесвто иждивенцев</label>
                                                <input
                                                    type="number"
                                                    className="payment-amount"
                                                    min={0} step="1" max={3}
                                                    value={paymentData.num_dependents}
                                                    onChange={(e) => updatePayment('num_dependents', e.target.value)}
                                                    required />
                                            </div>
                                        </div>
                                    </>
                                )} */}

                        </div>
                    )}


                    {/* Размер выплаты или страховой части */}
                    <div className="grid">
                        <div className="form-group">
                            <label>{paymentData.categoria !== 'insurance' ? 'Размер назначенной выплаты*' : 'Размер страховой части'}</label>
                            <input
                                type="number"
                                className="payment-amount"
                                min="0" step="0.01"
                                value={paymentData.amount}
                                onChange={(e) => updatePayment('amount', e.target.value)}
                                required />
                        </div>
                    </div>


                    {/* Есть ли перерасчет страховой части или просто выплаты */}
                    {(paymentData.categoria === PENSION_CATEGORIES_CHILDREN.departmental.raw
                        || paymentData.categoria === PENSION_CATEGORIES_CHILDREN.social_SPK.raw
                        || paymentData.categoria === PENSION_CATEGORIES_CHILDREN.social_disability.raw
                        || paymentData.categoria === 'insurance'
                        || paymentData.categoria === 'social'
                        || paymentData.categoria === 'departmental'
                        || paymentData.categoria === 'other') && (

                            <div>
                                <div className="checkbox-group">
                                    <input
                                        type="checkbox"
                                        id="recalculationCheck"
                                        checked={paymentData.is_recalculation}
                                        onChange={(e) => updatePayment('is_recalculation', e.target.checked)}
                                    />
                                    <label htmlFor="recalculationCheck">{paymentData.categoria === 'insurance' ? 'Есть перерасчет страховой части' : 'Есть перерасчет'}</label>
                                </div>

                                {paymentData.is_recalculation && (
                                    <div id="recalculatiionContainer" className="recalculatiion-container">
                                        {paymentData.recalculation?.map((recal, idx) => (
                                            <>
                                                <RecalculationForm
                                                    key={`recalc-${idx}-${recal.date || 'new'}`}
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


                            </div>
                        )}

                    {/* Если пенсия страховая, то есть ли фиксированная часть */}
                    <div>
                        {paymentData.categoria == "insurance" && (
                            <div className="checkbox-group">
                                <input
                                    type="checkbox"
                                    id="fixAmountCheck"
                                    checked={paymentData.is_fix_amoumt}
                                    onChange={(e) => updatePayment('is_fix_amoumt', e.target.checked)}
                                />
                                <label className="dop_check" htmlFor="fixAmountCheck">Есть фиксированная выплата</label>
                            </div>
                        )}

                        {paymentData.is_fix_amoumt && (
                            <>
                                <div className="grid">
                                    <div className="form-group">
                                        <label>Размер фиксированной выплаты</label>
                                        <input
                                            type="number"
                                            className="payment-amount"
                                            min="0" step="0.01"
                                            value={paymentData.amount_fix}
                                            onChange={(e) => updatePayment('amount_fix', e.target.value)}
                                            required />
                                    </div>
                                </div>

                                <div className="checkbox-group">
                                    <input
                                        type="checkbox"
                                        id="recalculationFixAmountCheck"
                                        checked={paymentData.is_recalculation_fix_amount}
                                        onChange={(e) => updatePayment('is_recalculation_fix_amount', e.target.checked)}
                                    />
                                    <label htmlFor="recalculationFixAmountCheck">Есть перерасчет фиксированной части</label>
                                </div>

                                {paymentData.is_recalculation_fix_amount && (
                                    <div id="recalculatiionFixAmountContainer" className="recalculatiion-container">
                                        {paymentData.recalculation_fix_amount?.map((recal, idx) => (
                                            <>
                                                <RecalculationForm
                                                    key={`fix-recalc-${idx}`}
                                                    paymentId={id}
                                                    recalIndex={idx}
                                                    index={idx + 1}
                                                    recalData={recal}
                                                    onUpdateRecalculation={updateRecalculationFixAmount}
                                                    onRemoveRecalculation={removeRecalculationFixAmount}
                                                />

                                            </>
                                        ))}

                                        <button
                                            type="button"
                                            className="btn btn-small"
                                            onClick={addRecalculationFixAmount}
                                        >
                                            + Добавить перерасчет
                                        </button>
                                    </div>
                                )}

                            </>
                        )}
                    </div>





                </div>
            </div>
        </>
    )
}


const RecalculationForm = ({
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

    if (!recalData) return null;

    return (
        <div className="container rec-container">
            <div className="recalculation-header">
                <h4>{index} перерасчет</h4>
                <button
                    type="button"
                    className="remove-period"
                    onClick={() => onRemoveRecalculation(paymentId, recalIndex)}
                >Удалить перерасчет</button>
            </div>
            <div className="grid-4">
                <div className="form-group">
                    <label>Дата перерасчета *</label>
                    <input
                        key={`key-date-${paymentId*Math.random()}}`}
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
                        key={`key-summa-${paymentId*Math.random()}}`}
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
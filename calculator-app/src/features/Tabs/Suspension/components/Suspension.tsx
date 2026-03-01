import { useSuspension } from "../hooks/useSuspension";
import { PeriodsSection } from "../../../../shared/components/PeriodSelectionForm/PeriodsSection";

export const Suspension = () => {
    const {
        store,
        navigate,
        ROUTES,
        updateStore,
        isSuspension,
        updateIsSuspension,
        PERSONA,
        PERIOD_TYPE,

    } = useSuspension();

    return (

        <div id="inpatient" className="tab-content">
            <h2>Периоды приостановок выплат</h2>

            <div className="simplified-section">
                <div className="checkbox-group">
                    <input
                        type="checkbox"
                        id="inpatientPeriodCheck"
                        checked={isSuspension}
                        onChange={(e) => updateIsSuspension(e.target.checked)}
                    />
                    <label htmlFor="inpatientPeriodCheck">Есть периоды приостановок выплат</label>
                </div>

                {isSuspension && (
                    <PeriodsSection persona={PERSONA.adult} typePeriod={PERIOD_TYPE.stop_payment} />
                )}
            </div>



            <div className="form-group">
                <button className="btn btn-secondary" id="backToParams" onClick={() => navigate(ROUTES.payments)}>Назад: Выплаты и периоды</button>
                <button className="btn btn-success" id="nextToPayments" onClick={() => navigate(ROUTES.results)}>Далее: Результаты</button>
            </div>
        </div>

    )
}
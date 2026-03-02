import { useSuspension } from "../hooks/useSuspension";
import { PeriodsSection } from "../../../../shared/components/PeriodSelectionForm/PeriodsSection";

export const Suspension = () => {
    const {
        navigate,
        ROUTES,
        PERSONA,
        PERIOD_TYPE,
        store,
        updateStore,
    } = useSuspension();

    return (

        <div id="inpatient" className="tab-content">
            <h2>Периоды приостановок выплат</h2>

            <div className="simplified-section">
                <div className="checkbox-group">
                    <input
                        type="checkbox"
                        id="inpatientPeriodCheck"
                        checked={store.is_suspension}
                        onChange={(e) =>updateStore('is_suspension',e.target.checked)}
                    />
                    <label htmlFor="inpatientPeriodCheck">Есть периоды приостановок выплат</label>
                </div>

                {store.is_suspension && (
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
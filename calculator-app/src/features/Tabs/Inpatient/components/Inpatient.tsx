import { useInpatient } from "../hooks/useInpatient";
import { PeriodsSection } from "../../../../shared/components/PeriodSelectionForm/PeriodsSection";
export const Inpatient = () => {
    const {
        store,
        navigate,
        ROUTES,
        updateStore,
        PERSONA,
        PERIOD_TYPE,

    } = useInpatient();
    return (

        <div id="inpatient" className="tab-content">
            <h2>Периоды пребывания в стационарх учреждениях</h2>

            <div className="simplified-section">
                <div className="checkbox-group">
                    <input
                        type="checkbox"
                        id="inpatientPeriodCheck"
                        checked={store.is_inpatient}
                        onChange={(e) => updateStore('is_inpatient', e.target.checked)}
                    />
                    <label htmlFor="inpatientPeriodCheck">Есть периоды размещения в стационарных учреждениях</label>
                </div>

                {store.is_inpatient && (
                    <PeriodsSection persona={PERSONA.adult} typePeriod={PERIOD_TYPE.inpatient} />
                )}
            </div>



            <div className="form-group">
                <button className="btn btn-secondary" id="backToParams" onClick={() => navigate(ROUTES.basic)}>Назад: Основные данные</button>
                <button className="btn btn-success" id="nextToPayments" onClick={() => navigate(ROUTES.payments)}>Далее: Выплаты и периоды</button>
            </div>
        </div>

    )
}
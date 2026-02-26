import { PeriodForm } from "./PeriodFrom";
import { usePeriods } from "./hooks/usePeriods";
import { PeriodsSectionProps } from "./types/periodType";
import { PERIOD_TYPE } from "../../constants/periodsName";

export const PeriodsSection = ({ persona, typePeriod }: PeriodsSectionProps) => {
    const {
        periods,
        addPeriod,
        updatePeriod,
        removePeriod
    } = usePeriods(persona, typePeriod);

    const handleAddPeriod = () => {
        addPeriod();
    };

    return (
        <div id="periodSection">
            <div className="form-group">
                {typePeriod === PERIOD_TYPE.registration && (
                    <>
                        <h3>Периоды регистрации в Москве <b>{persona}</b></h3>
                        <div className="info-box warning">
                            <p><strong>Важно:</strong> Укажите все периоды регистрации в Москве. Общая
                                продолжительность регистрации должна быть не менее 10 лет для получения ГСС.</p>
                        </div>
                    </>
                )}

                {typePeriod === PERIOD_TYPE.inpatient && (
                    <>
                        <h3>Периоды пребывания в стационарных учреждения</h3>
                    </>
                )}


                <div id="periodsContainer" className="periods-container">
                    {periods.map((period, index) => (
                        <PeriodForm
                            typePeriod={typePeriod}
                            key={period.id}
                            id={period.id}
                            index={index + 1}
                            periodData={period}
                            onUpdate={updatePeriod}
                            onRemove={removePeriod}
                        />
                    ))}
                </div>



                <button
                    className="btn"
                    id="addPeriod"
                    onClick={handleAddPeriod}
                >+ Добавить период</button>

            </div>
        </div>
    )
}
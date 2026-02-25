import { FormPeriodRegistration } from "./FromPeriodRegistration";
import { useArrayPeriodRegistration } from "../hooks/useArrayPeriodRegistration";

export const PeriodRegistrationSection = ({ persona }: {persona: string}) => {
    const {
        periods,
        addPeriod,
        updatePeriod,
        removePeriod
    } = useArrayPeriodRegistration(persona);

    const handleAddPeriod = () => {
        addPeriod();
    };


    return (
        <div id="registrationSection">
            <div className="form-group">
                <h3>Периоды регистрации в Москве {persona}</h3>
                <div className="info-box warning">
                    <p><strong>Важно:</strong> Укажите все периоды регистрации в Москве. Общая
                        продолжительность регистрации должна быть не менее 10 лет для получения ГСС.</p>
                </div>

                <div id="registrationPeriodsContainer" className="registration-periods-container">
                    {periods.map((period, index) => (   
                        <FormPeriodRegistration
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
                id="addRegistrationPeriod"
                onClick={handleAddPeriod}
                >+ Добавить период регистрации</button>


            </div>
        </div>
    )
}
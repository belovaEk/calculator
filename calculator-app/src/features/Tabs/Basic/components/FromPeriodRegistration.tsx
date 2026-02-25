import { usePeriodRegistration } from "../hooks/usePeriodRegistration"
import { FormPeriodRegistrationProps } from "../types/periodRegistration";
import { RegistrationPeriod } from "../../../../shared";

export const FormPeriodRegistration = ({
    id,
    index,
    periodData,
    onUpdate,
    onRemove
}: FormPeriodRegistrationProps) => {

    const updatePeriodRegistration = (field: keyof RegistrationPeriod, value: string) => {
        const updatedPeriod = {
            ...periodData,
            [field]: value
        };
        onUpdate(id, updatedPeriod);
    };

    const handleRemove = () => {
        onRemove(id);
    };

    const handleCurrentDate = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.checked) {
            updatePeriodRegistration('DKreg', new Date().toISOString().split('T')[0]);
        } else {
            updatePeriodRegistration('DKreg', '');
        }
    };

    return (
        <div className="registration-period">
            <div className="payment-header">
                <div className="payment-title">Период регистрации <span className="period-number">{index}</span></div>
                <button
                className="remove-period"
                type="button"
                onClick={handleRemove}
                >Удалить период</button>
            </div>

            <div className="payment-dates">
                <div className="form-group">
                    <label htmlFor={`DNreg-${id}`}>Дата начала регистрации *</label>
                    <input
                        id={`DNreg-${id}`}
                        type="date"
                        className="period-start"
                        value={periodData.DNreg}
                        required
                        onChange={(e) => updatePeriodRegistration('DNreg', e.target.value)}
                    ></input>
                </div>

                 <div className="form-group">
                    <label htmlFor={`DKreg-${id}`}>Дата окончания регистрации *</label>
                    <input
                        id={`DKreg-${id}`}
                        type="date"
                        className="period-end"
                        value={periodData.DKreg}
                        required
                        onChange={(e) => updatePeriodRegistration('DKreg', e.target.value)}
                    />
                </div>
            </div>

            <div className="date-options">
                <div className="date-option-group">
                    <input 
                        id={`current-${id}`}
                        type="checkbox"
                        className="current-date"
                        onChange={handleCurrentDate}
                        checked={periodData.DKreg === new Date().toISOString().split('T')[0]}
                    />
                    <label className="date-option-label" htmlFor={`current-${id}`}>
                        По настоящее время
                    </label>
                </div>
                {/* <div className="date-option-group">
                    <input type="checkbox" className="indefinite"></input>
                    <label className="date-option-label">Непрерывно (до прекращения)</label>
                </div> */}
            </div>
        </div>
    )
}
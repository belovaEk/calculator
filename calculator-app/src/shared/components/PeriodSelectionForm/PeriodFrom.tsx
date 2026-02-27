import { PeriodFromProps } from "./types/periodType";
import { DatePeriod } from "../..";

export const PeriodForm = ({
    typePeriod,
    id,
    index,
    periodData,
    onUpdate,
    onRemove
}: PeriodFromProps) => {

    const updatePeriod = (field: keyof DatePeriod, value: string) => {
        const updated = {
            ...periodData,
            [field]: value
        };
        onUpdate(id, updated);
    };

    const handleRemove = () => {
        onRemove(id);
    };

    const handleCurrentDate = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.checked) {
            updatePeriod('DK', new Date().toISOString().split('T')[0]);
        } else {
            updatePeriod('DK', '');
        }
    };

    return (
        <div className="date-period">
            <div className="payment-header">
                <div className="payment-title">Период ({typePeriod}) <span className="period-number">{index}</span></div>
                <button
                    className="remove-period"
                    type="button"
                    onClick={handleRemove}
                >Удалить период</button>
            </div>

            <div className="payment-dates">
                <div className="form-group">
                    <label htmlFor={`DN-${id}`}>Дата начала *</label>
                    <input
                        id={`DN-${id}`}
                        type="date"
                        className="period-start"
                        value={periodData.DN}
                        required
                        onChange={(e) => updatePeriod('DN', e.target.value)}
                    ></input>
                </div>

                <div className="form-group">
                    <label htmlFor={`DK-${id}`}>Дата окончания *</label>
                    <input
                        id={`DK-${id}`}
                        type="date"
                        className="period-end"
                        value={periodData.DK}
                        required
                        onChange={(e) => updatePeriod('DK', e.target.value)}
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
                        checked={periodData.DK === new Date().toISOString().split('T')[0]}
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
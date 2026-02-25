import { RegistrationPeriod } from "../../../../shared";


export interface FormPeriodRegistrationProps {
    id: number;
    index: number;
    periodData: RegistrationPeriod;
    onUpdate: (id: number, updatedPeriod: RegistrationPeriod) => void;
    onRemove: (id: number) => void;
}
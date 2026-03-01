import { DatePeriod } from "../../..";
import { personaType } from "../../../constants/people";
import { PeriodType } from "../../../constants/periodsName";

export interface PeriodFromProps {
    typePeriod: PeriodType;
    id: number;
    index: number;
    periodData: DatePeriod;
    onUpdate: (id: number, updatedPeriod: DatePeriod) => void;
    onRemove: (id: number) => void;
}



export interface PeriodsSectionProps {
    persona: personaType;
    typePeriod: PeriodType;
}
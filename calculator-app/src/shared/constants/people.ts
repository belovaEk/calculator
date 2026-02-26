export type personaType = 'ребенок' | 'законный представитель / кормилец' | ''

export const PERSONA: Record<string, personaType> ={
    children: 'ребенок',
    representative: 'законный представитель / кормилец',
    adult: '',
};


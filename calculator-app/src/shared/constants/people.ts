export type personaType = 'ребенок' | 'законный представитель' | 'кормилец' | ''

export const PERSONA: Record<string, personaType> ={
    children: 'ребенок',
    legal_representative: 'законный представитель',
    adult: '',
    breadwinner: 'кормилец',
};


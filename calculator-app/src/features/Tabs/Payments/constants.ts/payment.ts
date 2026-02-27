export const PENSION_CATEGORIES = {
    insurance_SPK: {
        raw: 'insurance_SPK',
        display: 'Страховая по СПК',
    },
    social_SPK: {
        raw: 'social_SPK',
        display: 'Социальная по СПК',
    },
    social_disability:{
        raw: 'social_disability',
        display: 'Социальная по инвалидности'
    }
}

export const PAYMENT_TYPE = {
    pension: {
        raw: 'pension',
        display: 'Пенсия'
    },
    edv: {
        raw: 'edv',
        display: 'ЕДВ'
    },
    egdv: {
        raw: 'egdv',
        display: 'ЕГДВ'
    },
    housin: {
        raw: 'housin',
        display: 'ЖКУ'
    },
    custom: {
        raw: 'custom',
        display: 'Другая выплата'
    }
} as const


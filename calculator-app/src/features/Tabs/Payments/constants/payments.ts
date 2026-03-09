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
    housing: {
        raw: 'housing',
        display: 'ЖКУ'
    },
    custom: {
        raw: 'custom',
        display: 'Другая выплата'
    }
} as const
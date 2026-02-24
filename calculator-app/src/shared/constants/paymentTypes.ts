import {
    PensionTypeKey,
    EdvTypeKey,
    EgdvTypeKey
} from '../types';

export const PENSION_TYPES: Record<PensionTypeKey, string> = {
    insurance_old_age: 'Страховая пенсия по старости',
    insurance_disability: 'Страховая пенсия по инвалидности',
    insurance_loss: 'Страховая пенсия по случаю потери кормильца',
    social_disability: 'Социальная пенсия по инвалидности',
    social_loss: 'Социальная пенсия по случаю потери кормильца',
    social_old_age: 'Социальная пенсия по старости',
    custom: 'Другая (указать вручную)'
} as const;

export const EDV_CATEGORIES: Record<EdvTypeKey, string> = {
    first_group: '1 группа',
    second_group: '2 группа / Дети-инвалиды',
    third_group: '3 группа',
    custom: 'Другая (указать вручную)'
} as const;

export const EGDV_CATEGORIES: Record<EgdvTypeKey, string> = {
    children_first_group: 'Инвалиды 1 группы, дети-инвалиды, уход',
    orphans_second_group: 'Инвалиды с детства 2 группы, сироты',
    pens_second_group_SPK: 'Пенсионеры по старости, инвалиды 2 группы, СПК',
    third_group: 'Инвалиды 3 группы',
    custom: 'Другая (указать вручную)'
} as const;
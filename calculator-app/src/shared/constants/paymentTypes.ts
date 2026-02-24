import {
    PensionTypeKey,
    EDVGroupKey,
    EGDVCategoryKey
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

export const EDV_GROUPS: Record<EDVGroupKey, string> = {
    '1 группа': '1 группа',
    '2 группа Дети-инвалиды': '2 группа / Дети-инвалиды',
    '3 группа': '3 группа',
    custom: 'Другая (указать вручную)'
} as const;

export const EGDV_CATEGORIES: Record<EGDVCategoryKey, string> = {
    'инвалиды 1 группы дети-инвалиды уход': 'Инвалиды 1 группы, дети-инвалиды, уход',
    'инвалиды с детства 2 группы сироты': 'Инвалиды с детства 2 группы, сироты',
    'пенсионеры по старости инвалиды 2 группы СПК': 'Пенсионеры по старости, инвалиды 2 группы, СПК',
    'инвалиды 3 группы': 'Инвалиды 3 группы',
    custom: 'Другая (указать вручную)'
} as const;
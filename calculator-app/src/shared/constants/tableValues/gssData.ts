import { YearlyData } from "../../types";

export const GSS_DATA: YearlyData = {
    2019: 19500,
    2020: 19500,
    2021: 20222,
    2022: 21193,
    2023: 23313,
    2024: 24500,
    2025: 25850,
    2026: 27401
} as const;

export type GSSYear = keyof typeof GSS_DATA;


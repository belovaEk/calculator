import { fetchPost } from "../../../../shared/api/http";
import { JsonDataWithIndex, PromiseI } from "../types/resultType";

export const getResults = async (jsonData: JsonDataWithIndex): Promise<PromiseI> => {
    return await fetchPost('/calculate', jsonData);
}
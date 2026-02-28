import { fetchGet } from "../../../../shared/api/http";
import { GlobalStoreParameterInterface } from "../../../../store/type";


export const getResults = async (allData: GlobalStoreParameterInterface): Promise<any> => {
    return await fetchGet('/');
}
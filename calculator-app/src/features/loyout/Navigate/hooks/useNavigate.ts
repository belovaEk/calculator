import { useNavigate, useLocation } from 'react-router-dom';
import { ROUTES } from '../../../../constants/routes';

export const useTabs = () => {
    const navigate = useNavigate();
    const location = useLocation();

    // Функция для определения активной вкладки по пути
    const getActiveTabFromPath = () => {
        if (location.pathname.includes('params')) return 'params';
        if (location.pathname.includes('basic')) return 'basic';
        if (location.pathname.includes('payments')) return 'payments';
        if (location.pathname.includes('results')) return 'results';
        return 'params'; // по умолчанию
    };

    const activeTab = getActiveTabFromPath();

    const tabs = [
        { id: 'params', label: 'Параметры ГСС и ПМП', route: ROUTES.params },
        { id: 'basic', label: 'Основные данные', route: ROUTES.basic },
        { id: 'payments', label: 'Выплаты и периоды', route: ROUTES.payments },
        { id: 'results', label: 'Результаты расчета', route: ROUTES.results }
    ];


    return {
        navigate,
        activeTab,
        tabs
    }
}

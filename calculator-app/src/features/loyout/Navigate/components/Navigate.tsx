
import { useTabs } from "../hooks/useNavigate";

export const Navigate = ()=> {

    const {
        navigate,
        activeTab,
        tabs
    } = useTabs();

  return (
    <div className="tabs">
      {tabs.map(tab => (
        <div
          key={tab.id}
          className={`tab ${activeTab === tab.id ? 'active' : ''}`}
          onClick={() => navigate(tab.route)}
        >
          {tab.label}
        </div>
      ))}
    </div>
  );
}
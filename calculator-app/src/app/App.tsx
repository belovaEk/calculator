import { BrowserRouter as Router } from 'react-router-dom';
import ScrollToTop from '../utils/scrollToTop';
import { GlobalStoreProvider } from '../store';
import Layout from '../features/loyout/Layout';
import { AppRoutes } from './appRoutes';


function App() {
  return (
    <Router>
      <GlobalStoreProvider>
        <Layout>
          <ScrollToTop />
          <AppRoutes />
        </Layout>
      </GlobalStoreProvider>
    </Router>
  );
}

export default App;
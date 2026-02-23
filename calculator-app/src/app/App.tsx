import React from 'react';
import Header from '../features/loyout/Header';
import Navigate from '../features/loyout/Navigate';
import { BrowserRouter as Router } from 'react-router-dom';

import Layout from '../features/loyout/Layout';
import { AppRoutes } from './appRoutes';


function App() {
  return (
    <>
    <Router>
      <Layout>
        <AppRoutes/>
      </Layout>
    </Router>
    </>
  );
}

export default App;
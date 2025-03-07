import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Layout from './layout/layout';
import ThemeSearch from './components/theme_search/theme_search';

const AppRoutes = () => {
  return (
    <Router>
      <Routes>
        {/* <Route path="/" element={<Layout><ThemeSearch /></Layout>} /> */}
        {/* <Route path="/cim-summary" element={<Layout><CIMSummary /></Layout>} /> */}
        <Route path="/theme-search" element={<Layout><ThemeSearch /></Layout>} />
        <Route path="*" element={<Navigate to="/theme-search" />} />
      </Routes>
    </Router>
  );
};

export default AppRoutes; 
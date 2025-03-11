import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import ThemeSearch from './components/theme_search/theme_search';
import CimSummary from './components/cim_summary/cim_summary';

const AppRoutes = () => {
  return (
    <Router>
      <Routes>
        {/* <Route path="/" element={<Layout><ThemeSearch /></Layout>} /> */}
        <Route path="/cim-summary" element={<CimSummary />} />
        <Route path="/theme-search" element={<ThemeSearch />} />
        <Route path="*" element={<Navigate to="/theme-search" />} />
      </Routes>
    </Router>
  );
};

export default AppRoutes; 
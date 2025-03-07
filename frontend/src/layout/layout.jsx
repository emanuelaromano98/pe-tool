import { Link, useNavigate, useLocation } from 'react-router-dom';
import './layout.css';

const Layout = ({ children }) => {
  const navigate = useNavigate();

  const currentPath = useLocation().pathname;

  return (
    <div className="layout">
      <header className="layout-header">
        <div className="nav-container">
          <div className="section-buttons">
            <button 
              className="btn-section" 
              onClick={() => navigate('/theme-search')}
              style={{ color: currentPath === '/theme-search' ? '#6772e5' : '#1a1f36' }}
            >
              Theme Search
            </button>
            <button 
              className="btn-section" 
              onClick={() => navigate('/cim-summary')}
              style={{ color: currentPath === '/cim-summary' ? '#6772e5' : '#1a1f36' }}
            >
              CIM Summary
            </button>
          </div>
        </div>
      </header>

      <main className="layout-main">
        {children}
      </main>
    </div>
  );
};

export default Layout;
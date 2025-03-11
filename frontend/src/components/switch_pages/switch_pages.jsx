import './switch_pages.css'
import { useNavigate } from 'react-router-dom'

function SwitchPages({activePage}) {
    const navigate = useNavigate();

    const handlePageChange = (page) => {
        navigate(`/${page}`);
    }

    return (
        <div className="switch-pages-container">
            <button className={`switch-pages-item ${activePage === "theme-search" ? "active" : ""}`} onClick={() => handlePageChange("theme-search")}>Theme Search</button>
            <button 
                className={`switch-pages-item ${activePage === "cim-summary" ? "active" : ""}`} 
                onClick={() => handlePageChange("cim-summary")}
            >
                CIM Summary
            </button>
        </div>
    )
}

export default SwitchPages;
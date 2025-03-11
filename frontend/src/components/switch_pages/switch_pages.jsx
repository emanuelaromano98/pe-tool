import './switch_pages.css'
import { useState } from 'react'
function SwitchPages() {

    const [activePage, setActivePage] = useState("theme-search")


    const handlePageChange = (page) => {
        setActivePage(page)
    }

    return (
        <div className="switch-pages-container">
            <button className={`switch-pages-item ${activePage === "theme-search" ? "active" : ""}`} onClick={() => handlePageChange("theme-search")}>Theme Search</button>
            <button className={`switch-pages-item ${activePage === "cim-summary" ? "active" : ""}`} onClick={() => handlePageChange("cim-summary")}>CIM Summary</button>
        </div>
    )
}
export default SwitchPages;
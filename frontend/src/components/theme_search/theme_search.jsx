import './theme_search.css'
import { useState, useEffect } from 'react'
import Select from 'react-select'
import useWebSocket from '../../useWebSocket'
import { useSelector, useDispatch } from 'react-redux'
import { setApiKey, resetApi } from '../../slices/mainSlice'
import { useNavigate } from 'react-router-dom'

function ThemeSearch() {

  const [theme, setTheme] = useState("")
  const [fromYear, setFromYear] = useState(new Date().getFullYear())
  const [toYear, setToYear] = useState(new Date().getFullYear())
  const [model, setModel] = useState("o1")
  const [formSubmitted, setFormSubmitted] = useState(false)
  const [formSubmittedClicked, setFormSubmittedClicked] = useState(false)
  const [submitError, setSubmitError] = useState("")
  const [reportGenerated, setReportGenerated] = useState(false)
  const [isAdvancedExpanded, setIsAdvancedExpanded] = useState(false)
  const currentYear = new Date().getFullYear()
  const [selectedCountries, setSelectedCountries] = useState([])
  const status = useWebSocket();
  const apiKey = useSelector((state) => state.main.apiKey)
  const dispatch = useDispatch()


  const baseAPIUrl = "http://127.0.0.1:8000"

  useEffect(() => {
    if (toYear < fromYear) {
      setToYear(fromYear)
    }
  }, [fromYear, toYear])

  const years = Array.from(
    { length: currentYear - (currentYear-10) + 1 },
    (_, i) => currentYear - i
  )

  const toYearOptions = Array.from(
    { length: currentYear+10 - fromYear + 1 },
    (_, i) => fromYear + i
  ).sort((a, b) => b - a)

  useEffect(() => {
    if (apiKey.trim() !== "" && 
        selectedCountries.length > 0 && 
        theme.trim() !== "" && 
        fromYear !== "" && 
        toYear !== "" && 
        formSubmittedClicked) {
      setSubmitError("")
    } else if (formSubmittedClicked) {
      if (apiKey.trim() === "" || 
      selectedCountries.length === 0 || 
      theme.trim() === "" || 
      fromYear === "" || 
      toYear === ""
    ) {
        setSubmitError("Please fill in all fields")
      }
    }
  }, [apiKey, theme, formSubmittedClicked, selectedCountries, fromYear, toYear])

  const handleSubmitForm = async (e) => {
    e.preventDefault()
    setFormSubmittedClicked(true)
    if (theme.trim() === "" || 
    apiKey.trim() === "" || 
    selectedCountries.length === 0 ||
    fromYear === "" ||
    toYear === "") {
      setSubmitError("Please fill in all fields")
      return
    }
    setFormSubmitted(true)
    try {
      const response = await fetch(`${baseAPIUrl}/generate-theme-report`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          theme: theme.trim(),
          model,
          api_key: apiKey.trim(),
          countries: selectedCountries.map(country => country.label),
          from_year: String(fromYear),
          to_year: String(toYear)
        }),
      })
      const data = await response.json()
      console.log(data)
      setReportGenerated(true)
    } catch (error) {
      console.error("Error in report generation:", error)
    }
  }

  const handleDownloadReport = (format) => {
    const url = `${baseAPIUrl}/download-theme-report?format=${format}`
    window.open(url, '_blank')
  }

  const handleReset = () => {
    setReportGenerated(false)
    setFormSubmittedClicked(false)
    setFormSubmitted(false)
    setTheme("")
    setModel("o1")
    dispatch(resetApi())
    setSubmitError("")
    setSelectedCountries([])
    setFromYear(new Date().getFullYear())
    setToYear(new Date().getFullYear())
  }

  const countryOptions = [
    { value: 'us', label: 'United States' },
    { value: 'uk', label: 'United Kingdom' },
    { value: 'eu', label: 'European Union' }
  ]

  const handleCountryChange = (selectedOptions) => {
    setSelectedCountries(selectedOptions || [])
  }

  const navigate = useNavigate();

  const handlePageChange = (page) => {
    navigate(`/${page}`);
  }

  return (
    <div>          
        <div className="general-container">
          <div className="app-container">
            <div className="switch-pages-container-outer">
            <div className="switch-pages-container">
            <button className={`switch-pages-item active`} >
                Theme Search
            </button>
            <button 
                className={`switch-pages-item`} 
                onClick={() => handlePageChange("cim-summary")}
            >
                CIM Summary
            </button>
        </div>      
          <form 
            autoComplete="off" 
            method="get"
            role="search"
            data-type="search"
            className="theme-search-form"
          >
            <label>
              <span>Theme Search</span>
              <input 
                className="theme-search-input"
                disabled={formSubmitted}
                style={
                  (theme.trim() === "" && formSubmittedClicked) 
                    ? { border: "1px solid red" } 
                    : {}
                }
                type="text" 
                value={theme} 
                onChange={(e) => setTheme(e.target.value)}
                placeholder="e.g. Technology"
              />
            </label>
            <label>
            </label>
            <div className="country-choice-section">
              <span>Country Choice</span>
              <div className="country-select-container"
                style={
                  (selectedCountries.length === 0 && formSubmittedClicked) 
                    ? { border: "1px solid red", borderRadius: "5px" } 
                    : {}
                }
              >
                <Select
                  isMulti
                  options={countryOptions}
                  value={selectedCountries}
                  onChange={handleCountryChange}
                  isDisabled={formSubmitted}
                  className="country-select"
                  classNamePrefix="country-select"
                  placeholder="Select countries..."
                  name="country-search"
                  id="country-search"
                  inputId="country-search-input"
                  aria-label="Search and select countries"
                  role="searchbox"
                  data-type="search"
                  data-private="false"
                />
              </div>
            </div>
            <label>
              <span>Time Period</span>
              <div className="time-period-container">
                <span>From</span>
                <select 
                  disabled={formSubmitted}
                  value={fromYear}
                  onChange={(e) => setFromYear(parseInt(e.target.value))}
                >
                  {years.map((year) => (
                    <option key={year} value={year}>{year}</option>
                  ))}
                </select>
                <span>To</span>
                <select 
                  disabled={formSubmitted}
                  value={toYear}
                  onChange={(e) => setToYear(parseInt(e.target.value))}
                >
                  {toYearOptions.map((year) => (
                    <option key={year} value={year}>{year}</option>
                  ))}
                </select>
              </div>
            </label>
            <label>
              <span>OpenAI API Key</span>
              <input 
                disabled={formSubmitted}
                style={
                  (apiKey.trim() === "" && formSubmittedClicked) 
                    ? { border: "1px solid red" } 
                    : {}
                }
                type="password" 
                value={apiKey} 
                onChange={(e) => dispatch(setApiKey(e.target.value))}
                placeholder="sk-..."
                />
            </label>
            <div className="advanced-settings-toggle" onClick={() => setIsAdvancedExpanded(!isAdvancedExpanded)}>
              <span className={`arrow ${isAdvancedExpanded ? 'expanded' : ''}`}>▶︎</span>
              <span className="advanced-settings-toggle-text">Advanced Settings</span>
            </div>
            <div className={`advanced-container ${isAdvancedExpanded ? 'expanded' : ''}`}>
              <label className="model-container">
                <div className="model-container-inner">
                  <span>LLM Model</span>
                  <select
                    disabled={formSubmitted}
                    value={model}
                    onChange={(e) => setModel(e.target.value)}
                  >
                    <option value="o1">GPT-o1</option>
                    <option value="gpt-4o-mini">GPT-4o-mini</option>
                    <option value="gpt-4o">GPT-4o</option>
                    <option value="o3-mini">GPT-o3-mini</option>
                  </select>
                </div>
              </label>
            </div>
            <button 
              disabled={formSubmitted}
              className="generate-report-button" 
              onClick={(e) => handleSubmitForm(e)} 
              type="submit"
            >
              Generate Report
            </button>
            {submitError && <div className="error">{submitError}</div>}
          </form> 
          </div>
          <div className="report-status-container" style={{ display: 'flex', 
            flexDirection: 'column', 
            alignItems: 'left', 
            padding: '10px', 
            borderRadius: '10px'}}>
            {formSubmitted && (
              <div className="report-container">
                <h3>Report Generation Status</h3>
                <div className="status-message" style={{ whiteSpace: 'pre-line' }}>
                  {status || "Generating reports..."}
                </div>
                {reportGenerated && (
                  <div className="download-report-container-outer">
                    <h4>Download File</h4>
                    <div className="download-report-container-inner">
                      <button onClick={() => handleDownloadReport("html")} className="download-report-button">HTML</button>
                      <button onClick={() => handleDownloadReport("pdf")} className="download-report-button">PDF</button>
                      <button onClick={() => handleDownloadReport("markdown")} className="download-report-button">Markdown</button>
                      <button onClick={() => handleDownloadReport("txt")} className="download-report-button">Text</button>
                    </div>
                  </div>
                )}
                {reportGenerated && (
                  <button 
                    onClick={() => handleReset()}
                    className="reset-button"
                  style={{ alignSelf: 'flex-start', marginTop: '10px' }}
                >
                    Reset
                  </button>
                )}
                </div>
            )} 
            
          </div>
        </div>
      </div>
      </div>
  )
}

export default ThemeSearch;

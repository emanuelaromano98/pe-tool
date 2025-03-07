import './theme_search.css'
import { useState, useEffect } from 'react'
import Select from 'react-select'

function ThemeSearch() {

  const [industry, setIndustry] = useState("")
  const [topics, setTopics] = useState([])
  const [fromYear, setFromYear] = useState(new Date().getFullYear())
  const [toYear, setToYear] = useState(new Date().getFullYear())
  // eslint-disable-next-line no-unused-vars
  const [topic, setTopic] = useState("")
  const [model, setModel] = useState("gpt-4o-2024-08-06")
  const [threshold, setThreshold] = useState(0.85)
  const [apiKey, setApiKey] = useState("")
  const [error, setError] = useState("")
  const [formSubmitted, setFormSubmitted] = useState(false)
  const [status, setStatus] = useState("");
  const [formSubmittedClicked, setFormSubmittedClicked] = useState(false)
  const [submitError, setSubmitError] = useState("")
  const [reportGenerated, setReportGenerated] = useState(false)
  const [isAdvancedExpanded, setIsAdvancedExpanded] = useState(false)
  const currentYear = new Date().getFullYear()
  const [selectedCountries, setSelectedCountries] = useState([])

  const baseAPIUrl = "http://localhost:8000"
  

  useEffect(() => {
    const ws = new WebSocket("ws://localhost:8000/ws/status");
    ws.onmessage = (event) => {
        setStatus(event.data);
    };
    return () => ws.close();
  }, []);

  const numbers = Array.from(
    { length: ((1.0 - 0.05) / 0.05) + 1 },
    (_, i) => Number((0.05 + (i * 0.05)).toFixed(2))
  )

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

  // eslint-disable-next-line no-unused-vars
  const handleAddTopic = (topic, e) => {
    e.preventDefault()
    if (error) {
      setError("")
    }
    if (topic.trim() !== "" && !topics.includes(topic)) {
      setTopics([...topics, topic])
      setTopic("")
    } else if (topic.trim() === "") {
      setError("Topic cannot be empty")
    } else {
      setError("Topic already exists")
    }
  }

  // eslint-disable-next-line no-unused-vars
  const handleRemoveTopic = (topic, e) => {
    e.preventDefault()
    setTopics(topics.filter((t) => t !== topic))
  }

  useEffect(() => {
    if (topics.length !== 0 && apiKey.trim() !== "" && industry.trim() !== "" && formSubmittedClicked) {
      setSubmitError("")
    } else if (formSubmittedClicked) {
      if (topics.length === 0) {
        setSubmitError("Please fill in all fields")
      } else if (apiKey.trim() === "") {
        setSubmitError("Please fill in all fields")
      } else if (industry.trim() === "") {
        setSubmitError("Please fill in all fields")
      }
    }
  }, [topics, apiKey, industry, formSubmittedClicked])


  const handleSubmitForm = async (e) => {
    e.preventDefault()
    setFormSubmittedClicked(true)
    if (industry.trim() === "" || topics.length === 0 || apiKey.trim() === "") {
      setSubmitError("Please fill in all fields")
      return
    }
    setFormSubmitted(true)
    try {
      const response = await fetch(`${baseAPIUrl}/generate-report`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          industry,
          topics,
          model,
          threshold,
          api_key: apiKey,
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
    const url = `${baseAPIUrl}/download-report?format=${format}`
    window.open(url, '_blank')
  }

  const handleReset = () => {
    setReportGenerated(false)
    setFormSubmittedClicked(false)
    setFormSubmitted(false)
    setIndustry("")
    setTopics([])
    setTopic("")
    setModel("gpt-4o-2024-08-06")
    setThreshold(0.85)
    setApiKey("")
    setError("")
    setStatus("")
    setSubmitError("")
    setSelectedCountries([])
  }

  const countryOptions = [
    { value: 'us', label: 'United States' },
    { value: 'uk', label: 'United Kingdom' },
    { value: 'eu', label: 'European Union' }
  ]

  const handleCountryChange = (selectedOptions) => {
    setSelectedCountries(selectedOptions || [])
  }

  return (
    <div className="general-container">
      <div className="app-container">
        <form 
          autoComplete="off" 
          method="get"
          role="search"
          data-type="search"
        >
          <label>
            <span>Theme Search</span>
            <input 
              style={
                (industry.trim() === "" && formSubmittedClicked) 
                  ? { border: "1px solid red" } 
                  : {}
              }
              type="text" 
              value={industry} 
              onChange={(e) => setIndustry(e.target.value)}
              placeholder="e.g. Technology"
            />
          </label>
          <label>
          </label>
          <div className="country-choice-section">
            <span>Country Choice</span>
              <Select
                isMulti
                options={countryOptions}
                value={selectedCountries}
                onChange={handleCountryChange}
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
          <label>
            <span>Time Period</span>
            <div className="time-period-container">
              <span>From</span>
              <select 
                value={fromYear}
                onChange={(e) => setFromYear(parseInt(e.target.value))}
              >
                {years.map((year) => (
                  <option key={year} value={year}>{year}</option>
                ))}
              </select>
              <span>To</span>
              <select 
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
                style={
                  (apiKey.trim() === "" && formSubmittedClicked) 
                    ? { border: "1px solid red" } 
                    : {}
                }
                type="password" 
                value={apiKey} 
                onChange={(e) => setApiKey(e.target.value)}
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
                  value={model}
                onChange={(e) => setModel(e.target.value)}
              >
                <option value="gpt-4o-2024-08-06">GPT-4o</option>
                <option value="gpt-4o-mini-2024-07-18">GPT-4o-mini</option>
                <option value="o3-mini-2025-01-31">GPT-o3-mini</option>
                <option value="gpt-4-turbo-2024-04-09">GPT-4-turbo</option>
                </select>
              </div>
              <div className="model-container-inner">
                <span>Filtering Model</span>
                <select
                  value={model}
                  onChange={(e) => setModel(e.target.value)}
              >
                  <option value="all-MiniLM-L6-v2">MiniLM</option>
                </select>
              </div>
            </label>
            <label>
              <span>Similarity Threshold</span>
              <select
                value={threshold}
                onChange={(e) => setThreshold(parseFloat(e.target.value))}
              >
                {numbers.map((number) => (
                  <option value={number}>{number}</option>
                ))}
              </select>
            </label>
          </div>
          <button className="generate-report-button" onClick={(e) => handleSubmitForm(e)} type="submit">Generate Report</button>
          {submitError && <div className="error">{submitError}</div>}
        </form>  
        <div className="report-status-container" style={{ display: 'flex', flexDirection: 'column', alignItems: 'left', padding: '10px', borderRadius: '10px' }}>
          {formSubmitted && (
            <div className="report-container">
              <h3>Report Generation Status</h3>
              <div className="status-message">
                {status || "Initializing..."}
              </div>
              {reportGenerated && (
                <div className="download-report-container-outer">
                  <h4>Download File</h4>
                  <div className="download-report-container-inner">
                    <button onClick={() => handleDownloadReport("html")} className="download-report-button">HTML</button>
                    <button onClick={() => handleDownloadReport("pdf")} className="download-report-button">PDF</button>
                    <button onClick={() => handleDownloadReport("markdown")} className="download-report-button">Markdown</button>
                  </div>
                </div>
              )}
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
      </div>
     
    </div>
  )
}

export default ThemeSearch;

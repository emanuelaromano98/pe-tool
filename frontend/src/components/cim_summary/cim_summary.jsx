import { useState, useEffect } from 'react'
import Select from 'react-select'
import useWebSocket from '../../useWebSocket'
import './cim_summary.css'
import { useSelector, useDispatch } from 'react-redux'
import { setApiKey, resetApi } from '../../slices/mainSlice'
import { useNavigate } from 'react-router-dom'

function CimSummary() {
  const navigate = useNavigate();
  const [model, setModel] = useState("o1")
  const [formSubmitted, setFormSubmitted] = useState(false)
  const [formSubmittedClicked, setFormSubmittedClicked] = useState(false)
  const [submitError, setSubmitError] = useState("")
  const [reportGenerated, setReportGenerated] = useState(false)
  const [isAdvancedExpanded, setIsAdvancedExpanded] = useState(false)
  const [filteringModel, setFilteringModel] = useState("all-MiniLM-L6-v2")
  const [threshold, setThreshold] = useState(0.85)

  const handlePageChange = (page) => {
    navigate(`/${page}`);
  }

  const numbers = Array.from(
    { length: ((1.0 - 0.05) / 0.05) + 1 },
    (_, i) => Number((0.05 + (i * 0.05)).toFixed(2))
  )


  const [selectedAnalysis, setSelectedAnalysis] = useState([
    { value: 'all', label: 'Select All' }
  ])
  const status = useWebSocket();
  const [fileName, setFileName] = useState("Upload File")

  const handleFileChange = (event) => {
    if (event.target.files[0]) {
      setFileName(event.target.files[0].name)
    }
  }

  const apiKey = useSelector((state) => state.main.apiKey)
  const dispatch = useDispatch()


  const baseAPIUrl = "http://10.128.0.3:8000"

  useEffect(() => {
    if (apiKey.trim() !== "" && 
        selectedAnalysis.length > 0 && 
        fileName !== "Upload File" &&
        formSubmittedClicked) {
      setSubmitError("")
    } else if (formSubmittedClicked) {
      if (apiKey.trim() === "" || 
      selectedAnalysis.length === 0 ||
      fileName === "Upload File"
    ) {
        setSubmitError("Please fill in all fields")
      }
    }
  }, [apiKey, formSubmittedClicked, selectedAnalysis, fileName])

  const handleSubmitForm = async (e) => {
    e.preventDefault()
    setFormSubmittedClicked(true)

    const fileInput = document.getElementById('fileInput');
    if (!fileInput.files[0] || apiKey.trim() === "" || selectedAnalysis.length === 0) {
      setSubmitError("Please fill in all fields")
      return
    }

    setFormSubmitted(true)
    try {
      const formData = new FormData()
      formData.append('file', fileInput.files[0])
      formData.append('model', model)
      formData.append('filtering_model', filteringModel)
      formData.append('threshold', threshold.toString())
      formData.append('api_key', apiKey.trim())
      formData.append('title_file', fileInput.files[0].name + "_" + Math.random().toString(36).substring(2, 15))
      formData.append('analysis_type', JSON.stringify(
        selectedAnalysis.map(analysis => analysis.value)
      ))

      const response = await fetch(`${baseAPIUrl}/generate-cim-report`, {
        method: 'POST',
        body: formData,
      })
      const data = await response.json()
      console.log(data)
      setReportGenerated(true)
    } catch (error) {
      console.error("Error in report generation:", error)
      setSubmitError("Error generating report")
      setFormSubmitted(false)
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
    setModel("o1")
    dispatch(resetApi())
    setSubmitError("")
    setSelectedAnalysis([
      { value: 'all', label: 'Select All' }
    ])
  }

  const analysisOptions = [
    { value: 'all', label: 'Select All' },
    { value: 'fh', label: 'Founding & Headquarters' },
    { value: 'bo', label: 'Business Overview' },
    { value: 'cb', label: 'Customer Base' },
    { value: 'vp', label: 'Value Proposition' },
    { value: 'cc', label: 'Customer Concentration' },
    { value: 'gb', label: 'Geographic Breakdown' },
    { value: 'ka', label: 'Key Assets' },
    { value: 'eo', label: 'Employee Overview' },
    { value: 'fb', label: 'Financial Breakdown' }
  ]

  const handleAnalysisChange = (selectedOptions) => {
    console.log("calling handleanalysischange")
    if (selectedOptions?.some(option => option.value === 'all') 
        && selectedOptions.length > 1
        && selectedOptions[0].value === 'all'
    ) {
      setSelectedAnalysis(selectedOptions.filter(option => option.value !== 'all'))
    } else if (selectedOptions?.some(option => option.value === 'all') 
        && selectedOptions.length > 1
        && selectedOptions[0].value !== 'all'
    ) {
        setSelectedAnalysis(selectedOptions.filter(option => option.value === 'all'))
    } else if (selectedOptions.length===0){
        setSelectedAnalysis({ value: 'all', label: 'Select All' })
    } else {
      setSelectedAnalysis(selectedOptions)
    }
  }

  return (
    <div>    
      <div className="general-container">
        <div className="app-container">
          <div className="switch-pages-container-outer">
            <div className="switch-pages-container">
              <button 
                  className={`switch-pages-item`} 
                  onClick={() => handlePageChange("theme-search")}
              >
                  Theme Search
              </button>
              <button className={`switch-pages-item active`} >
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
            
            <label className="file-upload-label">
              <span>Upload CIM Document</span>
              <div className="file-upload-container" style={{
                backgroundColor: fileName !== "Upload File" && "white",
                border: (fileName === "Upload File" && formSubmittedClicked) ? "1px solid red" : "1px solid #ddd",
              }}>
                <span className="file-upload-label-text">
                    {fileName}
                </span>
                <input 
                  onChange={handleFileChange}
                  type="file" 
                  disabled={formSubmitted}
                  id="fileInput"
                  className="file-upload-input"
                  accept=".pdf"
                  style={{ display: 'none' }}  
                />
              </div>
            </label>
            <label>
            </label>
            <div className="country-choice-section">
              <span>Select Analysis</span>
              <div className="country-select-container"
                style={
                  (selectedAnalysis.length === 0 && formSubmittedClicked) 
                    ? { border: "1px solid red", borderRadius: "5px" } 
                    : {}
                }
              >
                <Select
                  isMulti
                  options={analysisOptions}
                  value={selectedAnalysis}
                  onChange={handleAnalysisChange}
                  isDisabled={formSubmitted}
                  className="analysis-select"
                  classNamePrefix="analysis-select"
                  placeholder="Select analysis..."
                  name="analysis-search"
                  id="analysis-search"
                  inputId="analysis-search-input"
                  aria-label="Search and select analysis"
                  role="searchbox"
                  data-type="search"
                  data-private="false"
                />
              </div>
            </div>
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
              <label className="model-container">
                <div className="model-container-inner">
                    <span>Filtering Model</span>
                        <select
                            disabled={formSubmitted}
                            value={filteringModel}
                            onChange={(e) => setFilteringModel(e.target.value)}
                        >
                            <option value="all-MiniLM-L6-v2">MiniLM</option>
                            <option value="sentence-t5-base">T5 Base</option>
                            <option value="paraphrase-albert-small-v2">ALBERT</option>
                            <option value="multi-qa-mpnet-base-dot-v1">MPNet-QA</option>
                        </select>
                </div>
                <div className="model-container-inner">
                    <span>Similarity Threshold</span>
                    <select
                    value={threshold}
                    onChange={(e) => setThreshold(parseFloat(e.target.value))}
                    >
                    {numbers.map((number) => (
                        <option value={number}>{number}</option>
                    ))}
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

export default CimSummary;
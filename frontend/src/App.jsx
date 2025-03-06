import './App.css'
import { useState, useEffect } from 'react'

function App() {

  const [industry, setIndustry] = useState("")
  const [topics, setTopics] = useState([])
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
  }


  return (
    <div className="general-container">
      <h1>Market Mapping Generator</h1>
      <div className="app-container">
        <form>
          <label>
            <span>Industry Name</span>
            <input 
              style={
                (industry.trim() === "" && formSubmittedClicked) 
                  ? { border: "1px solid red" } 
                  : {}
              }
              type="text" 
              value={industry} 
              onChange={(e) => setIndustry(e.target.value)}
              placeholder="e.g. Healthcare, Technology, Finance"
            />
          </label>
          <label>
            <span>Topics</span>
            <div className="topics-container">
              <input 
                style={
                  (topics.length === 0 && formSubmittedClicked) 
                    ? { border: "1px solid red" } 
                    : {}
                }
                type="text" 
                value={topic} 
                onChange={(e) => setTopic(e.target.value)}
                placeholder="Enter topic"
              />
              <button className="add-topic-button" onClick={(e) => handleAddTopic(topic, e)}>Add</button>
            </div>
            <div className="topics-list">
              {topics.map((topic, index) => (
                <span className="single-topic" key={index}>
                  {topic}
                  <button 
                    className="remove-topic" 
                    onClick={(e) => handleRemoveTopic(topic, e)}
                    style={{ outline: 'none' }}
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                      <path d="M18 6L6 18M6 6l12 12"/>
                    </svg>
                  </button>
                </span>

                ))}
            </div>
            {error && <p className="error">{error}</p>}
          </label>
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

export default App

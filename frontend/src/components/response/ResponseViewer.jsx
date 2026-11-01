import { useState } from "react"

function ResponseViewer() {
  const [activeTab, setActiveTab] = useState("Body")

  return (
    <section className="panel response-panel">
      <div className="response-heading">
        <div className="response-title"><h2>Response</h2></div>
      </div>
      <div className="editor-tabs response-tabs" role="tablist" aria-label="Response data">
        {["Body", "Headers"].map((tab) => (
          <button
            key={tab}
            role="tab"
            aria-selected={activeTab === tab}
            className={activeTab === tab ? "active" : ""}
            onClick={() => setActiveTab(tab)}
          >
            {tab}
          </button>
        ))}
      </div>
      <div className="response-empty-state">
        <h3>No response yet</h3>
        <p>{activeTab === "Body" ? "Send a request to view its response." : "Response headers will appear here when available."}</p>
      </div>
    </section>
  )
}

export default ResponseViewer

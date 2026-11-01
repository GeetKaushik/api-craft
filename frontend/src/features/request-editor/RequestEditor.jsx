import { useState } from "react"
import { Plus, Send, ShieldCheck } from "lucide-react"
import RequestTabs from "./RequestTabs.jsx"

function RequestEditor({ onNotice }) {
  const [activeTab, setActiveTab] = useState("Params")
  const [method, setMethod] = useState("GET")
  const [url, setUrl] = useState("")

  return (
    <section className="panel request-editor">
      <div className="url-bar">
        <select className={`method-select method-${method.toLowerCase()}`} value={method} onChange={(event) => setMethod(event.target.value)} aria-label="HTTP method">
          <option>GET</option><option>POST</option><option>PUT</option><option>PATCH</option><option>DELETE</option>
        </select>
        <input aria-label="Request URL" value={url} onChange={(event) => setUrl(event.target.value)} placeholder="Enter a request URL" spellCheck="false" />
        <button className="primary-button send-button" onClick={() => onNotice("Not implemented yet. No request was sent.")}><Send size={15} /> Send</button>
      </div>
      <RequestTabs activeTab={activeTab} onSelect={setActiveTab} />
      <RequestTabContent activeTab={activeTab} onNotice={onNotice} />
    </section>
  )
}

function RequestTabContent({ activeTab, onNotice }) {
  if (activeTab === "Params" || activeTab === "Headers") {
    const label = activeTab === "Params" ? "parameter" : "header"
    return (
      <div className="key-value-table">
        <div className="key-value-heading"><span>KEY</span><span>VALUE</span><span>DESCRIPTION</span><span /></div>
        <button className="add-row-button" onClick={() => onNotice(`Adding a ${label} is not implemented yet.`)}>
          <Plus size={14} /> Add {label}
        </button>
      </div>
    )
  }
  if (activeTab === "Body") {
    return <textarea className="request-body-code request-body-input" aria-label="Request body" placeholder="Request body is empty." />
  }
  return (
    <div className="auth-placeholder">
      <ShieldCheck size={17} />
      <span><strong>Authorization is not configured</strong><small>Authorization controls are not implemented yet.</small></span>
      <button className="secondary-button" onClick={() => onNotice("Authorization is not implemented yet.")}>Not implemented</button>
    </div>
  )
}

export default RequestEditor

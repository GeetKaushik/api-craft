import { ArrowRight, Folder, Import, Plus, Send, Sparkles } from "lucide-react"
import RecentRequests from "./RecentRequests.jsx"

function WelcomeDashboard({ onCreateRequest, onOpenModal }) {
  return (
    <div className="dashboard-view">
      <div className="welcome-header">
        <div>
          <div className="eyebrow"><Sparkles size={14} /> API CRAFT</div>
          <h1>Welcome to API Craft</h1>
          <p>Your workspace for building, testing, and organizing APIs.</p>
        </div>
        <button className="primary-button" onClick={onCreateRequest}><Plus size={16} /> Create new request</button>
      </div>
      <div className="quick-actions">
        <button className="quick-action" onClick={onCreateRequest}>
          <span className="quick-action-icon accent-icon"><Send size={16} /></span>
          <span><strong>New request</strong><small>Start with a blank request</small></span>
          <ArrowRight size={15} />
        </button>
        <button className="quick-action" onClick={() => onOpenModal("collection")}>
          <span className="quick-action-icon green-icon"><Folder size={16} /></span>
          <span><strong>New collection</strong><small>Organize related requests</small></span>
          <ArrowRight size={15} />
        </button>
        <button className="quick-action" onClick={() => onOpenModal("import")}>
          <span className="quick-action-icon amber-icon"><Import size={16} /></span>
          <span><strong>Import collection</strong><small>Bring in an API definition</small></span>
          <ArrowRight size={15} />
        </button>
      </div>
      <RecentRequests />
    </div>
  )
}

export default WelcomeDashboard

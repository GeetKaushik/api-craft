import { ArrowRight } from "lucide-react"

function RecentRequests() {
  return (
    <section className="panel recent-panel">
      <div className="panel-heading">
        <div><h2>Recent activity</h2><p>Your latest requests and activity</p></div>
        <span className="text-button recent-view-disabled" aria-disabled="true">View all <ArrowRight size={14} /></span>
      </div>
      <div className="recent-empty-state">
        <h3>No recent activity</h3>
        <p>No requests yet. Your saved requests and recent activity will appear here.</p>
      </div>
    </section>
  )
}

export default RecentRequests

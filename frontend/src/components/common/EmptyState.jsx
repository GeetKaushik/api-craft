import { FileCode2 } from "lucide-react"

function EmptyState({ title, description }) {
  return (
    <div className="empty-state-wrap">
      <div className="empty-state">
        <span className="empty-illustration"><FileCode2 size={25} /></span>
        <h1>{title}</h1>
        <p>{description}</p>
      </div>
    </div>
  )
}

export default EmptyState
